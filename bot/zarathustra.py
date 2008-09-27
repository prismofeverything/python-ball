import sys
import socket
import string
import re

import text
import bot

class Zarathustrabot(bot.MarkovBot):
    def __init__(self):
        bot.MarkovBot.__init__(self, 'Zarathustrabot', 'zarathustra.txt', 'Z', True)
    

if __name__ == "__main__":
    z = Zarathustrabot()
    z.process()
