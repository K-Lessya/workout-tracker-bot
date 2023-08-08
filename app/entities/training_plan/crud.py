from mongoengine import *
from app.entities.training_plan.training_plan import DbTrainingDay, DbTrainingPlan
from app.entities.single_file.models import Client


def get_training_days(client_id: int):
    client = Client.objects(tg_id=client_id).first()
    training_plan = client.training_plan
    return training_plan.days
