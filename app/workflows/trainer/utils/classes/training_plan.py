from app.entities.exercise.exercise import *


class PlanExercise:
    exercise: Exercise
    num_runs: int
    num_repeats: int

    def __init__(self, exercise: Exercise):
        self.exercise = exercise

    def add_runs(self, num_runs):
        self.num_runs = num_runs

    def add_repeats(self, num_repeats):
        self.num_repeats = num_repeats


class TrainingDay:
    day_number: int
    exercises: list[PlanExercise]

    def __init__(self):
        self.exercises = []
    def add_exercise(self, exercise: PlanExercise):
        self.exercises.append(exercise)



class TrainingPlan:
    days = list[TrainingDay]

    def __init__(self):
        self.days = []

    def add_day(self, day: TrainingDay):
        self.days.append(day)
