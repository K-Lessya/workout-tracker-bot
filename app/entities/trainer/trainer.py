from mongoengine import *


class Question(EmbeddedDocument):
    text = StringField()
    type = IntField(min_value=0, max_value=2)
    answers = ListField(StringField)
    selected_answer = IntField()


class Questionnaire(EmbeddedDocument):
    questions = EmbeddedDocumentListField(Question)


class Trainer(Document):
    tg_id = IntField(unique=True)
    tg_username = StringField()
    name = StringField()
    surname = StringField()
    visibility = BooleanField()
    photo_link = StringField()
    questionnaire = EmbeddedDocumentField(Questionnaire)