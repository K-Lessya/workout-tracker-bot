from mongoengine import *
from .exercise import BodyPart, MuscleGroup, Exercise


def create_body_part(body_part: BodyPart):
    body_part.save()
    return True


def get_all_body_parts():
    return BodyPart.objects()


def create_muscle_group(muscle_group: MuscleGroup):
    muscle_group.save()
    return True


def get_all_muscle_groups():
    return MuscleGroup.objects


def create_exercise(exercise: Exercise):
    exercise.save()
    return True

def update_exercise_muscle_groups(exercise: Exercise, muscle_group: MuscleGroup):
    exercise.muscle_groups.append(muscle_group)
    exercise.save()

