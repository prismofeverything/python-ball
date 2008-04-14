import pygame
import utility
import interface

def okay():
    d = w, h = 1000, 600

    ak = interface.Interface(d)

    a = 50
    c = 50
    for b in range(10, 100, 5):
        ak.drawText((c, a, 10, b), utility.Color((1.0, 0.9, 0.2)), "what the fuck?" + str(b), 15)
        a += b
        if a > h:
            a = 0
            c += 200

    pygame.display.update()

    return ak
