import sys
import socket
import string
import re

import text
import bot

class Zarathustrabot(bot.Bot):
    def __init__(self, channel='#instrument'):
        bot.Bot.__init__(self, 'Zarathustrabot', 'zarathustra.txt', 'Z', channel)

if __name__ == "__main__":
    z = Zarathustrabot("#instrument")
    z.join()
