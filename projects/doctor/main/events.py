import json
import pika
from django.conf import settings
from main.models import Doctor


class DoctorCreationEvent:
    def __init__(self, doctor: Doctor, password: str) -> None:
        self.doctor = doctor
        self.password = password

    def to_json(self) -> str:
        return json.dumps({
            "national_id": self.doctor.national_id,
            "name": self.doctor.name,
            "password": self.password,
        })


class EventProducer:

    def broadcast_doctor_creation(self, event: DoctorCreationEvent):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.EVENT_QUEUES["host"]))
        channel = connection.channel()

        doctor_settings = settings.EVENT_QUEUES["doctor"]
        doctor_exchange = doctor_settings["exchange"]
        channel.exchange_declare(
            exchange=doctor_exchange, exchange_type='fanout')

        channel.basic_publish(exchange=doctor_exchange, routing_key='',
                              body=event.to_json())
        connection.close()
