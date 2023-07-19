from mongoengine import *


class Exercise(Document):
    name = StringField(required=True)
    photo_link = StringField()
    video_link = StringField()
    description = StringField()


class TrainingExercise(EmbeddedDocument):
    exercise = ReferenceField(Exercise, required=True)
    num_repeats = IntField()
    num_runs = IntField()


class ClientTrainingExercise(TrainingExercise):
    weight = IntField()
    video_link = StringField()
    comment = StringField()


class TrainingDay(EmbeddedDocument):
    day_number = IntField(required=True)
    training_exercises = EmbeddedDocumentListField(TrainingExercise, required=True)


class TrainingPlan(EmbeddedDocument):
    days = EmbeddedDocumentListField(TrainingDay)


class Training(EmbeddedDocument):
    date = DateField(required=True)
    day_number = IntField(required=True)
    training_exercises = EmbeddedDocumentListField(ClientTrainingExercise)


class Client(Document):
    tg_id = StringField()
    tg_username = StringField(required=True)
    name = StringField()
    surname = StringField()
    weight = FloatField()
    height = IntField()
    training_plan = EmbeddedDocumentField(TrainingPlan)
    trainings = EmbeddedDocumentListField(Training)


class Trainer(Document):
    tg_id = StringField()
    tg_username = StringField(required=True)
    name = StringField()
    surname = StringField()
    clients = ListField(ReferenceField(Client))

