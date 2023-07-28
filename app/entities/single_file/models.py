from mongoengine import *
from ..exercise.exercise import ClientTrainingExercise, Exercise, PlanTrainingExercise


class TrainingDay(EmbeddedDocument):
    day_number = IntField(required=True)
    training_exercises = EmbeddedDocumentListField(PlanTrainingExercise, required=True)


class TrainingPlan(EmbeddedDocument):
    days = EmbeddedDocumentListField(TrainingDay)


class Training(EmbeddedDocument):
    date = DateField(required=True)
    name = StringField()
    day_number = IntField()
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
    training_plan = EmbeddedDocumentField(TrainingPlan)
    trainings = EmbeddedDocumentListField(Training)


class ClientRequests(Document):
    client = ReferenceField(Client, unique=True)
    trainers = ListField(ReferenceField(Trainer))


class TrainerRequests(Document):
    trainer = ReferenceField(Trainer, unique=True)
    clients = ListField(ReferenceField(Client))


