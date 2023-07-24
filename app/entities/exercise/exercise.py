from mongoengine import *


class BodyPart(Document):
    name = StringField()


class MuscleGroup(Document):
    name = StringField()
    body_part = ReferenceField(BodyPart)


class Exercise(Document):
    name = StringField()
    video_link = StringField()
    photo_link = StringField()
    muscle_groups = ListField(ReferenceField(MuscleGroup))


class PlanTrainingExercise(EmbeddedDocument):
    exercise = ReferenceField(Exercise, required=True)
    num_repeats = IntField()
    num_runs = IntField()

    meta = {"allow_inheritance": True}


class ClientTrainingExercise(PlanTrainingExercise):
    weight = FloatField()
    video_link = StringField()
    comment = StringField()

