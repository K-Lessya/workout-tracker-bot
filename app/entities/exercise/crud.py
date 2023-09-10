from mongoengine import *
from .exercise import BodyPart, MuscleGroup, Exercise


def create_body_part(body_part: BodyPart):
    body_part.save()
    return True


def get_body_part_by_id(body_part_id: str):
    return BodyPart.objects(id=body_part_id).first()


def get_all_body_parts(trainer_id) -> list[BodyPart]:
    return BodyPart.objects(trainer=trainer_id)


def create_muscle_group(muscle_group: MuscleGroup):
    muscle_group.save()
    return True


def get_muscle_groups_by_body_part(body_part: BodyPart):
    return MuscleGroup.objects(body_part=body_part)


def get_muscle_group_by_id(muscle_group_id: str):
    return MuscleGroup.objects(id=muscle_group_id).first()


def create_exercise(exercise: Exercise):
    exercise.save()
    return True

def get_exercises_by_muscle_group(muscle_group: MuscleGroup):
    return Exercise.objects(muscle_groups=muscle_group)

def get_exercise_by_id(exercise_id: str):
    return Exercise.objects(id=exercise_id).first()

def update_exercise_muscle_groups(exercise: Exercise, muscle_group: MuscleGroup):
    exercise.muscle_groups.append(muscle_group)
    exercise.save()

def get_all_exercises():
    exercises = Exercise.objects()
    return exercises