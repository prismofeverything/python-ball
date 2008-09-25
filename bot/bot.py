import sys
import socket
import string
import re

import text


def has(line, msg):
    return line.find(msg) != -1

class Bot:
    def __init__(self, nick, source, trigger, channel='#instrument'):
        self.markov = text.markovBook(source)
        self.trigger = re.compile(trigger)

        self.host = 'irc.freenode.net'
        self.port = 6667
        self.nick = nick
        self.ident = 'spanglerbot'
        self.realname = 'spangler'
        self.owner = 'patchwork'
        self.channel = channel

        self.readbuffer = ''

        self.s = socket.socket()
        self.s.connect((self.host, self.port))

    def generate(self):
        return ' '.join(self.markov.generate())

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
                self.send('JOIN ' + self.channel)
            if has(line, 'PRIVMSG'):
                self.parse_msg(line)

            line = line.split()
            if(line[0] == 'PING'):
                self.send('PONG '+line[1])

    def respond(self, sender, statement):
        response = 'PRIVMSG ' + self.channel + ' :' + sender[0] + ': ' + statement
        print response

        self.send(response)

    def parse_msg(self, line):
        complete = line[1:].split(':', 1)
        info = complete[0].split(' ')
        msg = complete[1]
        sender = info[0].split('!')

        if self.trigger.search(msg) is not None:
            statement = self.generate()
            parts = self.break_msg(statement)

            for part in parts:
                self.respond(sender, part)

    def break_msg(self, whole):
        if len(whole) > 300:
            parts = whole.split()
            sections = ['']
            index = 0

            for part in parts:
                if len(sections[index]) > 400:
                    sections.append(part)
                    index += 1
                else:
                    sections[index] += ' ' + part

            return sections
        else:
            return [whole]

