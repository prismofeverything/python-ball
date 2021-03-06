import random

class Wedge:
    def __init__(self, content, portion):
        self.content = content
        self.portion = portion

class Wheel:
    def __init__(self):
        self.wedges = []
        self.totalPortion = 0.0

    def retrieve(self, content):
        for wedge in self.wedges:
            if wedge.content == content:
                return wedge

        return None

    def add(self, content, portion):
        wedge = self.retrieve(content)

        if not wedge:
            self.wedges.append(Wedge(content, portion))
        else:
            wedge.portion += portion

        self.totalPortion += portion

    def remove(self, content):
        wedge = self.retrieve(content)
        if wedge:
            self.wedges.remove(wedge)

    def spin(self):
        if len(self.wedges):
            choice = random.random() * self.totalPortion
            index = 0

            while choice > self.wedges[index].portion:
                choice -= self.wedges[index].portion
                index += 1

            return self.wedges[index].content
        else:
            return None
