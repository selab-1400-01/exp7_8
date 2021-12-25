from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import json
import pika
import pika.exceptions
from time import sleep
from main.models import Doctor, Patient, Prescription


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

        self.channel.basic_consume(
            queue=self.prescription_queue,
            on_message_callback=self.__consume_prescription,
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
        prescription_settings = settings.EVENT_QUEUES["prescription"]
        doctor_exchange = doctor_settings["exchange"]
        patient_exchange = patient_settings["exchange"]
        prescription_exchange = prescription_settings["exchange"]
        self.doctor_queue = doctor_settings["queue"]
        self.patient_queue = patient_settings["queue"]
        self.prescription_queue = prescription_settings["queue"]

        channel.exchange_declare(
            exchange=doctor_exchange, exchange_type='fanout')
        channel.exchange_declare(
            exchange=patient_exchange, exchange_type='fanout')
        channel.exchange_declare(
            exchange=prescription_exchange, exchange_type='fanout')

        channel.queue_declare(queue=self.doctor_queue, durable=True)
        channel.queue_declare(queue=self.patient_queue, durable=True)
        channel.queue_declare(queue=self.prescription_queue, durable=True)

        channel.queue_bind(exchange=doctor_exchange, queue=self.doctor_queue)
        channel.queue_bind(exchange=patient_exchange, queue=self.patient_queue)
        channel.queue_bind(exchange=prescription_exchange,
                           queue=self.prescription_queue)

    def __consume_doctor(self, ch, method, properties, body):
        self.stdout.write("Received doctor in prescription.")
        doctor_info = json.loads(body)
        if "password" in doctor_info:
            del doctor_info["password"]
        Doctor.objects.get_or_create(national_id=doctor_info["national_id"], name=doctor_info["name"])

    def __consume_patient(self, ch, method, properties, body):
        self.stdout.write("Received patient in prescription.")
        patient_info = json.loads(body)
        if "password" in patient_info:
            del patient_info["password"]
        Patient.objects.get_or_create(national_id=patient_info["national_id"], name=patient_info["name"])

    def __consume_prescription(self, ch, method, properties, body):
        self.stdout.write("Received prescription in prescription.")
        prescription_info = json.loads(body)
        doctor_national_id = prescription_info["doctor_national_id"]
        patient_national_id = prescription_info["patient_national_id"]
        drugs_list = prescription_info["drugs_list"]
        comment = prescription_info["comment"]
        doctor = Doctor.objects.get(national_id=doctor_national_id)
        patient = Patient.objects.get(national_id=patient_national_id)
        Prescription.objects.create(
            doctor=doctor, patient=patient, drugs_list=drugs_list, comment=comment)
