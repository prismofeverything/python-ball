import Tkinter
from Tkconstants import *

tk = Tkinter.Tk()
frame = Tkinter.Frame(tk)
frame.pack(fill=BOTH, expand=1)

class Tkanvas:
    def __init__(self, width, height):
        self.canvas = Tkinter.Canvas(frame,
                                     width=width,
                                     height=height,
                                     background="Red")
        self.canvas.pack(fill=BOTH, expand=1)

    def start(self):
        tk.mainloop()


