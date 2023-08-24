from mongoengine import *
from app.entities.exercise.exercise import *

class DbTrainingDay(EmbeddedDocument):
    name = StringField()
    training_exercises = EmbeddedDocumentListField(PlanTrainingExercise, required=True)


class DbTrainingPlan(EmbeddedDocument):
    days = EmbeddedDocumentListField(DbTrainingDay)