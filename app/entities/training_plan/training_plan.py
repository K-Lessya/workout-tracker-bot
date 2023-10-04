from mongoengine import *
from app.entities.exercise.exercise import *

class DbTrainingDay(EmbeddedDocument):
    name = StringField(required=True)
    training_exercises = EmbeddedDocumentListField(PlanTrainingExercise, default=[])


class DbTrainingPlan(EmbeddedDocument):
    date = DateField()
    days = EmbeddedDocumentListField(DbTrainingDay, default=[])
    published = BooleanField(required=True, default=False)