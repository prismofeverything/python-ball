import sys
import socket
import string
import re

import text

def has(line, message):
    return line.find(message) != -1

channel_name = re.compile("#[^ ]+")

class Bot:
    def __init__(self, nick):
        self.host = 'irc.freenode.net'
        self.port = 6667
        self.nick = nick
        self.ident = 'nietzschebot'
        self.realname = 'flux'
        self.owner = 'patchwork'
        self.channels = {}

        self.connected = False
        self.processing = False

        self.readbuffer = ''

        self.connect()

    def send(self, message):
        self.s.send(message + '\n')

    def connect(self):
        self.s = socket.socket()
        self.s.connect((self.host, self.port))

        self.connected = True

    def identify(self):
        self.send('NICK ' + self.nick)
        self.send('USER ' + self.ident + ' ' + self.host + ' bla :' + self.realname)

    def process(self):
        self.processing = True
        self.identify()

        while self.processing:
            line = self.s.recv(500).rstrip()

            print line

            if len(self.channels) == 0:
                self.join("#dog")
            if has(line, 'PRIVMSG'):
                self.parse_message(line)

            parts = line.split()
            if len(parts) > 0 and parts[0] == 'PING':
                self.send('PONG ' + parts[1])
            
    def join(self, channel):
        self.channels[channel] = True
        self.send('JOIN ' + channel)

    def leave(self, channel):
        del self.channels[channel]
        self.send('LEAVE ' + channel)

    def quit(self):
        for channel in self.channels.keys:
            self.leave(channel)

        self.processing = False
        self.connected = False

    def respond(self, channel, message):
        response = 'PRIVMSG ' + channel + ' :' + message
        print '<' + self.nick + '> ' +  message

        self.send(response)

    def parse_message(self, line):
        complete = line[1:].split(':', 1)
        info = complete[0].split(' ')
        message = complete[1]
        sender = info[0].split('!')[0]
        channel = info[2]

        print '<' + sender + '> ' +  message

        self.handle_message(channel, sender, message)

    def handle_message(self, channel, sender, message):
        pass

    def send_message(self, channel, message):
        parts = self.break_message(message)

        for part in parts:
            self.respond(channel, part)

    def break_message(self, message):
        """ breaks down a response if it is too long for one IRC message """
        if len(message) > 300:
            parts = message.split()
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
            return [message]



class MarkovBot(Bot):
    def __init__(self, nick, source, trigger):
        Bot.__init__(self, nick)

        self.markov = text.markovBook(source)
        self.trigger = re.compile(trigger)

    def generate(self):
        return ' '.join(self.markov.generate())

    def handle_message(self, channel, sender, message):
        if self.trigger.search(message) is not None:
            if has(statement, "join")
            statement = self.generate()
            message = sender + ": " + statement
            self.send_message(channel, message)

