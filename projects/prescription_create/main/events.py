import json
import pika
from django.conf import settings


class PrescriptionCreationEvent:
    def __init__(self, prescription, doctor_national_id) -> None:
        self.prescription = prescription
        self.doctor_national_id = doctor_national_id

    def to_json(self) -> str:
        return json.dumps({
            "doctor_national_id": self.doctor_national_id,
            "patient_national_id": self.prescription.national_id,
            "drugs_list": self.prescription.drugs_list,
            "comment": self.prescription.comment,
        })


class EventProducer:

    def broadcast_prescription_creation(self, event: PrescriptionCreationEvent):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.EVENT_QUEUES["host"]))
        channel = connection.channel()

        prescription_settings = settings.EVENT_QUEUES["prescription"]
        prescription_exchange = prescription_settings["exchange"]
        channel.exchange_declare(
            exchange=prescription_exchange, exchange_type='fanout')

        channel.basic_publish(exchange=prescription_exchange, routing_key='',
                              body=event.to_json())
        connection.close()
