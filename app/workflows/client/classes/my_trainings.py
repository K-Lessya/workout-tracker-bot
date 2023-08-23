class MyTrainings:
    count = 4
    start_pos: int
    end_pos: int
    length: int

    def __init__(self, start_pos, end_pos, length):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.length = length

    def update(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos


class MyTrainingsOption:
    text: str
    target: str
    option: str
    def __init__(self, text, target, option):
        self.text = text
        self.target = target
        self.option = option

