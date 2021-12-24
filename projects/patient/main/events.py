import json
import pika
from django.conf import settings
from main.models import Patient


class PatientCreationEvent:
    def __init__(self, patient: Patient, password: str) -> None:
        self.patient = patient
        self.password = password

    def to_json(self) -> str:
        return json.dumps({
            "national_id": self.patient.national_id,
            "name": self.patient.name,
            "password": self.password,
        })


class EventProducer:

    def broadcast_patient_creation(self, event: PatientCreationEvent):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()

        patient_settings = settings.EVENT_QUEUES["patient"]
        patient_exchange = patient_settings["exchange"]
        channel.exchange_declare(
            exchange=patient_exchange, exchange_type='fanout')

        channel.basic_publish(exchange=patient_exchange, routing_key='',
                              body=event.to_json())
        connection.close()
