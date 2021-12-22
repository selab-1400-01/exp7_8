from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import pika


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
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
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
        self.stdout.write(str(body))

    def __consume_patient(self, ch, method, properties, body):
        self.stdout.write("Received patient.")
        self.stdout.write(str(body))
