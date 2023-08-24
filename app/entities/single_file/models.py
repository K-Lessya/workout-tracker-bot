from mongoengine import *
from ..exercise.exercise import ClientTrainingExercise, Exercise, PlanTrainingExercise
from ..training_plan.training_plan import *

class Training(EmbeddedDocument):
    name = StringField()
    date = DateField(required=True)
    training_exercises = EmbeddedDocumentListField(ClientTrainingExercise)


class Trainer(Document):
    tg_id = IntField(unique=True)
    tg_username = StringField()
    name = StringField()
    surname = StringField()
    visibility = BooleanField()
    photo_link = StringField()


class Client(Document):
    tg_id = IntField(unique=True)
    tg_username = StringField()
    phone_number = StringField()
    visibility = BooleanField()
    photo_link = StringField()
    name = StringField()
    surname = StringField()
    weight = FloatField()
    height = IntField()
    trainer = ReferenceField(Trainer)
    training_plan = EmbeddedDocumentField(DbTrainingPlan)
    trainings = EmbeddedDocumentListField(Training)


class ClientRequests(Document):
    client = ReferenceField(Client, unique=True)
    trainers = ListField(ReferenceField(Trainer))


class TrainerRequests(Document):
    trainer = ReferenceField(Trainer, unique=True)
    clients = ListField(ReferenceField(Client))


