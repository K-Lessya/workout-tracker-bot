from mongoengine import *
from ..training_plan.training_plan import *
from app.entities.trainer.trainer import Trainer


class Training(EmbeddedDocument):
    name = StringField()
    date = DateField(required=True)
    training_exercises = EmbeddedDocumentListField(ClientTrainingExercise)


class Client(Document):
    tg_id = IntField(unique=True)
    tg_username = StringField()
    lang = StringField()
    phone_number = StringField()
    visibility = BooleanField()
    photo_link = StringField()
    name = StringField()
    surname = StringField()
    weight = FloatField()
    height = IntField()
    trainer = ReferenceField(Trainer)
    custom_exercises = ListField(ReferenceField(Exercise))
    training_plans = EmbeddedDocumentListField(DbTrainingPlan)
    trainings = EmbeddedDocumentListField(Training)


class ClientRequests(Document):
    client = ReferenceField(Client, unique=True)
    trainers = ListField(ReferenceField(Trainer))


class TrainerRequests(Document):
    trainer = ReferenceField(Trainer, unique=True)
    clients = ListField(ReferenceField(Client))


