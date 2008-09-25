import utility.DivTree

# class Measure:
#     def __init__(self, root, duration=1.0):
#         self.root = root
#         self.duration = duration



# class MeasureList:
#     def __init__(self):
#         self.measures = []


# Does it really need Measures if a measure is just a node of divisions?
# The entire piece is a single duration, with the measures being
# the first divisions of the unit node.


class Cursor:
    def __init__(self, node):
        self.node = node

    def up(self):
        if self.node.over:
            self.node = self.node.over

    
