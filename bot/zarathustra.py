import sys
import socket
import string

import text


def has(line, msg):
    return line.find(msg) != -1

class Zarathustrabot:
    def __init__(self):
        self.markov = text.markovBook('bot/zarathustra.txt')

        self.host = 'irc.freenode.net'
        self.port = 6667
        self.nick = 'Zarathustrabot'
        self.ident = 'nietzschebot'
        self.realname = 'Zarathustra'
        self.owner = 'patchwork'
        self.channelinit = '#instrument'

        self.readbuffer = ''

        self.s = socket.socket()
        self.s.connect((self.host, self.port))

    def send(self, msg):
        self.s.send(msg+'\n')

    def join(self):
        self.send('NICK '+self.nick)
        self.send('USER '+self.ident+' '+self.host+' bla :'+self.realname)

        while True:
            line=self.s.recv(500)
            line = line.rstrip()

            print line

            if has(line, 'Welcome'):
                self.send('JOIN '+self.channelinit)
            if has(line, 'PRIVMSG'):
                self.parse_msg(line)

            line = line.split()
            if(line[0] == 'PING'):
                self.send('PONG '+line[1])

    def parse_msg(self, line):
        complete = line[1:].split(':', 1)
        info = complete[0].split(' ')
        msg = complete[1]
        sender = info[0].split('!')

        if msg[0:3] == '>>>':
            response = 'PRIVMSG '+self.channelinit+' :'+sender[0]+': '+' '.join(self.markov.generate())
            print response

            self.send(response)


