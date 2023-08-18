import datetime
from app.workflows.trainer.utils.classes.training_plan import PlanExercise


class ClientTrainingExerciseSchema(PlanExercise):
    weight: float
    video_link: str
    comment: str

    def __init__(self, exercise):
        super().__init__(exercise=exercise)

    def add_weight(self, weight):
        self.weight = weight

    def add_video_link(self, video_link):
        self.video_link = video_link



class ClientTrainingSchema:
    date: datetime.date
    training_exercises: list[ClientTrainingExerciseSchema]

    def __init__(self):
        self.date = datetime.date.today()
        self.training_exercises = []

    def add_exercise(self, exercise):
        self.training_exercises.append(exercise)


