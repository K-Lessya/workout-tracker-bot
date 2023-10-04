from datetime import date
from mongoengine import *
from app.entities.training_plan.training_plan import DbTrainingDay, DbTrainingPlan
from app.entities.single_file.models import Client
from app.entities.exercise.exercise import PlanTrainingExercise


def get_training_days(client_id: int, plan_id: int):
    client = Client.objects(tg_id=client_id).first()
    training_plan = client.training_plans[plan_id]
    return training_plan.days


def create_new_plan(client: Client):
    client.training_plans.append(DbTrainingPlan(days=[], published=False, date=date.today()))
    client.save()


def get_single_plan(client_id: int, idx: int):
    client = Client.objects(tg_id=client_id).first()
    return client.training_plans[idx]


def get_plans(client: Client):
    return client.training_plans


def create_day(client_id: Client, name: str, plan_id: int):
    client = Client.objects(tg_id=client_id).first()
    client.training_plans[plan_id].days.append(DbTrainingDay(name=name, training_exercises=[]))
    client.save()


def get_last_plan_exercise(client_id: int, plan_id: int):
    client = Client.objects(tg_id=client_id).first()
    exercise = client.training_plans[plan_id].days[-1].training_exercises[-1]
    return exercise

def get_plan_exercise(client_id: int, plan_id: int, day_id: int, exercise_id: int):
    client = Client.objects(tg_id=client_id).first()
    return client.training_plans[plan_id].days[day_id].training_exercises[exercise_id]

def get_day_exercises(client_id: int, plan_id: int, day_id: int):
    client = Client.objects(tg_id=client_id).first()
    return client.training_plans[plan_id].days[day_id].training_exercises

def add_new_exercise_to_day(client_id: int, plan_id: int, day_id: int, exercise):
    client = Client.objects(tg_id=client_id).first()
    client.training_plans[plan_id].days[day_id].training_exercises.append(PlanTrainingExercise(exercise=exercise))
    client.save()

def get_client_active_plans(client_id: int):
    client = Client.objects(tg_id=client_id).first()

    active_plans = [plan for plan in client.training_plans if plan.published == True]
    print(active_plans)
    return active_plans


def create_last_plan_exercise_num_runs(client_id: int, num_runs: int, plan_id: int, day_id):
    client = Client.objects(tg_id=client_id).first()
    exercise = client.training_plans[plan_id].days[day_id].training_exercises[-1]
    exercise.num_runs = num_runs
    client.save()


def create_last_plan_exercise_num_repeats(client_id: int, num_repeats: int, plan_id: int, day_id):
    client = Client.objects(tg_id=client_id).first()
    exercise = client.training_plans[plan_id].days[day_id].training_exercises[-1]
    exercise.num_repeats = num_repeats
    client.save()


def edit_exercise_num_runs(client_id: int, plan_id: int, day_id: int, exercise_id: int, num_runs: int):
    client = Client.objects(tg_id=client_id).first()
    client.training_plans[plan_id].days[day_id].training_exercises[exercise_id].num_runs = num_runs
    client.save()


def edit_exercise_num_repeats(client_id: int, plan_id: int, day_id: int, exercise_id: int, num_repeats: int):
    client = Client.objects(tg_id=client_id).first()
    client.training_plans[plan_id].days[day_id].training_exercises[exercise_id].num_repeats = num_repeats
    client.save()


def edit_exercise_trainer_note(client_id: int, plan_id: int, day_id: int, exercise_id: int, trainer_note: str):
    client = Client.objects(tg_id=client_id).first()
    client.training_plans[plan_id].days[day_id].training_exercises[exercise_id].trainer_note = trainer_note
    client.save()

def publish_new_plan(client_id: int, plan_id: int):
    client = Client.objects(tg_id=client_id).first()
    for plan in client.training_plans:
        if plan.published:
            plan.published = False
    client.training_plans[plan_id].published = True
    client.save()

