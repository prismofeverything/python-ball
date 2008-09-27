import sys
import os
import socket
import string
import re
import math

import text

def has(line, message):
    return line.find(message) != -1

channel_name = re.compile("#[^ ]+")
non_punctuation = re.compile("[^.,!?]+")

class Bot:
    def __init__(self, nick, logging=False):
        self.host = 'irc.freenode.net'
        self.port = 6667
        self.nick = nick
        self.identity = 'nietzschebot'
        self.realname = 'flux'
        self.owner = 'patchwork'
        self.channels = {}

        self.connected = False
        self.processing = False
        self.logging = logging
        self.logs = {}

        self.readbuffer = ''

    def send(self, message):
        self.s.send(message + '\n')

    def connect(self):
        """if used as an IRC bot, you need to open the socket with connect()
        and then start the loop with process()"""
        self.s = socket.socket()
        self.s.connect((self.host, self.port))

        self.connected = True

    def identify(self):
        self.send('NICK ' + self.nick)
        self.send('USER ' + self.identity + ' ' + self.host + ' bla :' + self.realname)
        self.send('NICKSERV IDENTIFY ' + self.identity)

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
            
    def open_log(self, path, channel):
        try:
            os.makedirs('logs/channels')
        except:
            print "already exists"

        self.logs[channel] = open(path + channel[1:], 'a')

    def join(self, channel):
        if self.logging:
            self.open_log('logs/channels/', channel)
        self.channels[channel] = True

        self.send('JOIN ' + channel)

    def leave(self, channel):
        if self.logging:
            self.logs[channel].close()
            del self.logs[channel]
        del self.channels[channel]

        self.send('PART ' + channel)

    def quit(self):
        for channel in self.channels.keys:
            self.leave(channel)

        self.processing = False
        self.connected = False

    def respond(self, channel, message):
        response = 'PRIVMSG ' + channel + ' :' + message

        self.log(channel, self.nick, message)
        self.send(response)

    def log(self, channel, sender, message):
        log = '<' + sender + '> ' +  message
        print log

        if self.logging:
            self.logs[channel].write(log + '\n')
            self.logs[channel].flush()

    def parse_message(self, line):
        complete = line[1:].split(':', 1)
        info = complete[0].split(' ')
        message = complete[1]
        sender = info[0].split('!')[0]
        channel = info[2]

        self.log(channel, sender, message)
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
    def __init__(self, nick, source, trigger, logging=False):
        Bot.__init__(self, nick, logging)

        self.markov = text.markovBook(source)
        self.trigger = re.compile(trigger)

    def generate(self):
        return self.markov.generate()

    def handle_message(self, channel, sender, message):
        frequencies = []
        for word in message.split():
            clean = non_punctuation.search(word).group(0)
            if self.markov.has(clean):
                node = self.markov.nodes[clean]
                frequencies.append([node.data, float(node.occurrences) / self.markov.totalAtoms])
        frequencies.sort(lambda a, b: cmp(a[1], b[1]))

        if self.trigger.search(message) is not None:
            if len(frequencies) > 0:
                statement = self.markov.expandFrom(frequencies[0][0])
            else:
                statement = self.generate()

            reply = sender + ": " + statement
            self.send_message(channel, reply)

            if has(message, "join"):
                try:
                    new_channel = channel_name.search(message).group(0)
                    self.join(new_channel)
                except:
                    pass
            elif has(message, "leave"):
                try:
                    old_channel = channel_name.search(message).group(0)
                    self.leave(old_channel)
                except:
                    pass
            elif has(message, "topic"):
                topic_channel = channel
                try:
                    topic_channel = channel_name.search(message).group(0)
                except:
                    pass
                self.send("TOPIC " + topic_channel + " " + self.markov.generateN(11))
            elif has(message, "quit"):
                self.quit()
            

