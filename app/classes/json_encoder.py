import json
from json import JSONEncoder, JSONDecoder


class ObjEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__




