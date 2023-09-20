from enum import Enum
from .translations_en import EnglishTranslations
from .translations_ru import RussianTranslations


class Languages(Enum):
    RU = 'Русский'
    EN = 'English'

translations = {
    Languages.RU.name: RussianTranslations,
    Languages.EN.name: EnglishTranslations
}
