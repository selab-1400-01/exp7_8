from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import json
import pika
import pika.exceptions
from time import sleep
from main.models import PatientId


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Starting queue listening...")

        self.__setup()

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

        patient_settings = settings.EVENT_QUEUES["patient"]
        patient_exchange = patient_settings["exchange"]
        self.patient_queue = patient_settings["queue"]

        channel.exchange_declare(
            exchange=patient_exchange, exchange_type='fanout')

        channel.queue_declare(queue=self.patient_queue, durable=True)

        channel.queue_bind(exchange=patient_exchange, queue=self.patient_queue)

    def __consume_patient(self, ch, method, properties, body):
        self.stdout.write("Received patient in prescription creation.")
        patient_info = json.loads(body)
        national_id = patient_info["national_id"]
        PatientId.objects.get_or_create(national_id=national_id)
