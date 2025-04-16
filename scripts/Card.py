class Card:

    def __init__(self, color=None, value=None, name=None):
        self.color = color
        self.value = value
        self.name = name

    def get_card(self):
        return f"{self.name} {self.color}"

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def get_value(self):
        return self.value
