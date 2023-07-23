from mongoengine import *


class Exercise(Document):
    name = StringField(required=True)
    photo_link = StringField()
    video_link = StringField()
    description = StringField()


class TrainingExercise(EmbeddedDocument):
     # exercise = ReferenceField(Exercise, required=True)
    name = StringField()
    num_repeats = IntField()
    num_runs = IntField()

    meta = {"allow_inheritance": True}


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
    name = StringField()
    day_number = IntField()
    training_exercises = EmbeddedDocumentListField(ClientTrainingExercise)





class Trainer(Document):
    tg_id = IntField()
    tg_username = StringField()
    name = StringField()
    surname = StringField()
    visibility = BooleanField()
    photo_link = StringField()

class Client(Document):
    tg_id = IntField()
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

