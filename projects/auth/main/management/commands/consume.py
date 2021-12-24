from threading import Thread
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User, Group
import json
import pika
import pika.exceptions
from time import sleep


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Starting queue listening...")

        self.__setup()

        self.channel.basic_consume(
            queue=self.doctor_queue,
            on_message_callback=self.__consume_doctor,
            auto_ack=True)

        self.channel.basic_consume(
            queue=self.patient_queue,
            on_message_callback=self.__consume_patient,
            auto_ack=True)

        self.stdout.write("Going to consume messages...")
        self.channel.start_consuming()

    def __setup(self):
        while True:
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=settings.EVENT_QUEUES["host"]))
                break
            except pika.exceptions.AMQPConnectionError:
                self.stdout.write("Couldn't connect.")
                sleep(1)
                pass

        self.channel = channel = connection.channel()

        doctor_settings = settings.EVENT_QUEUES["doctor"]
        patient_settings = settings.EVENT_QUEUES["patient"]
        doctor_exchange = doctor_settings["exchange"]
        patient_exchange = patient_settings["exchange"]
        self.doctor_queue = doctor_settings["queue"]
        self.patient_queue = patient_settings["queue"]

        channel.exchange_declare(
            exchange=doctor_exchange, exchange_type='fanout')
        channel.exchange_declare(
            exchange=patient_exchange, exchange_type='fanout')

        channel.queue_declare(queue=self.doctor_queue, durable=True)
        channel.queue_declare(queue=self.patient_queue, durable=True)

        channel.queue_bind(exchange=doctor_exchange, queue=self.doctor_queue)
        channel.queue_bind(exchange=patient_exchange, queue=self.patient_queue)

    def __consume_doctor(self, ch, method, properties, body):
        self.stdout.write("Received doctor.")
        user = self.__get_or_create_user_by_message(body)
        group, _ = Group.objects.get_or_create(name="doctors")
        user.groups.add(group)
        user.save()

    def __consume_patient(self, ch, method, properties, body):
        self.stdout.write("Received patient.")
        self.__get_or_create_user_by_message(body)

    def __get_or_create_user_by_message(self, body: bytes) -> User:
        national_id, password = Command.__get_national_id_and_pass(body)
        user, created = User.objects.get_or_create(username=national_id)
        if created:
            self.stdout.write(f"User created. Username = {user.username}")

        user.set_password(password)
        user.save()
        return user

    def __get_national_id_and_pass(body: bytes) -> tuple[str, str]:
        user_info = json.loads(body)
        return user_info["national_id"], user_info["password"]
