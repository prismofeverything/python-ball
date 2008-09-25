    

class Note:
    def __init__(self, scale, over, step=0, octave=0):
        self.scale = scale
        self.over = over
        self.divisions = []
        self.step = step
        self.octave = octave
        self.threaded = 0
        self.threading = 0

    def __repr__(self):
        def print_note(note, level, rep):
            space = ""
            for l in range(level):
                space += " "
                
            rep += space + "scale: " + str(note.scale) + "\n"
            rep += space + "step: " + str(note.step) + "\n"
            rep += space + "octave: " + str(note.octave) + "\n"
            rep += space + "divisions: \n"

            for d in note.divisions:
                rep = print_note(d, level+1, rep)

            rep += "\n"
            return rep

        return print_note(self, 0, "")

    def __getitem__(self, index):
        return self.divisions[index]

    def divide(self, number):
        divisions = self.divisions[:number]

        for d in range(number - len(divisions)):
            note = Note(self.scale, self)
            divisions.append(note)

        self.divisions = divisions

    def path(self):
        def find_path(note, p):
            if note.over == 0: return p
            else:
                index = note.over.divisions.index(note)
                return find_path(note.over, p.append(index))

        return find_path(self, []).reverse()

    def duration(self):
        def climb(note, dur):
            if note.over == 0: return dur
            else:
                index = note.over.divisions.index(note)
                return duration(over, dur.append(len(note.over.divisions)))

        return climb(self, []).reverse()
        
    def find(self, path):
        if path == []:
            return self
        else:
            index = path[0]
            if index < 0:
                if self.over == 0: return []
                else: return self.over.find(path[1:])
            elif index >= len(self.divisions):
                return []
            else:
                note = self.divisions[index]
                return note.find(path[1:])

    def set(self, path, note):
        if path == []:
            self.scale = note.scale
            self.divisions = note.divisions
            self.step = note.step
            self.octave = note.octave
        else:
            index = path[0]

            if index < 0:
                if self.over == 0:
                    self.over = Note(self.scale, 0)
                self.over.set(path[1:], note)
            elif index >= len(self.divisions):
               self.divide(index+1)

            division = self.divisions[index]
            division.set(path[1:], note)

    def first(self):
        if len(self.divisions) == 0:
            return self
        else:
            return self.divisions[0].first()

    def last(self):
        if len(self.divisions) == 0:
            return self
        else:
            return self.divisions[len(self.divisions)-1].last()

    def next(self):
        if self.over == 0: return self
        else:
            index = self.over.divisions.index(self)

            if index == len(self.over.divisions) - 1:
                return self.over.next()
            else:
                return self.over[index + 1].first()

    def previous(self):
        if self.over == 0: return self
        else:
            index = self.over.divisions.index(self)

            if index == 0:
                return self.over.previous()
            else:
                return self.over[index - 1].last()


def listToNote(notelist):
    
