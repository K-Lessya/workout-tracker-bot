from mongoengine import *
from app.entities.trainer.trainer import Trainer


class BodyPart(Document):
    name = StringField()
    trainer = ReferenceField(Trainer)


class MuscleGroup(Document):
    name = StringField()
    body_part = ReferenceField(BodyPart)


class Exercise(Document):
    name = StringField()
    media_link = StringField()
    media_type = StringField()
    photo_link = StringField()
    muscle_groups = ListField(ReferenceField(MuscleGroup))
    trainer = ReferenceField(Trainer)


class PlanTrainingExercise(EmbeddedDocument):
    exercise = ReferenceField(Exercise, required=True)
    num_repeats = IntField()
    num_runs = IntField()
    trainer_note = StringField()

    meta = {"allow_inheritance": True}


class ClientTrainingExercise(PlanTrainingExercise):
    weight = FloatField()
    video_link = StringField()
    comment = StringField()
    client_note = StringField()

