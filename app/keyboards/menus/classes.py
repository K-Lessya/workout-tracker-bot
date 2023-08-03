class MenuOption:
    text: str
    target: str
    option: str
    def __init__(self, text: str, target: str):
        self.text = text
        self.target = target