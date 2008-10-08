import sys
import os
import socket
import string
import re
import math

import text

def has(line, message):
    return line.find(message) != -1

class Channel:
    def __init__(self, name):
        self.name = name
        self.members = []

    def member_join(self, member):
        self.members.append(member)

    def member_leave(self, member):
        if member in self.members:
            self.members.remove(member)

    def member_nick(self, member, nick):
        if member in self.members:
            self.members.remove(member)
            self.members.append(nick)

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
        self.channel_logs = {}
        self.member_logs = {}

        self.readbuffer = ''
        self.handlers = {}

        self.re_sender = re.compile('^:(\w+)(![^ ]*)?')
        self.re_channel = re.compile("#[^ \r\n]+")
        self.re_non_punctuation = re.compile("[^.,!?]+")

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

    def open_log(self, path, subject):
        try:
            os.makedirs(path)
        except:
            print "already exists"

        return open(path + subject, 'a')

    def join(self, channel):
        if self.logging:
            self.channel_logs[channel] = self.open_log('logs/channels/', channel[1:])
        new_channel = Channel(channel)
        self.channels[channel] = new_channel

        self.send('JOIN ' + channel)

    def leave(self, channel):
        if self.logging:
            self.channel_logs[channel].close()
            del self.channel_logs[channel]
        del self.channels[channel]

        self.send('PART ' + channel)

    def quit(self):
        for channel in self.channels.keys():
            self.leave(channel)

        self.processing = False
        self.connected = False

    def respond(self, channel, message):
        response = 'PRIVMSG ' + channel + ' :' + message

        self.log(channel, self.nick, message)
        self.send(response)

    def log(self, channel, sender, message):
        if message[:7] == 'ACTION ':
            log = "* " + sender + " " + message[7:]
        else:
            log = '<' + sender + '> ' +  message
        print log

        if self.logging:
            self.channel_logs[channel].write(log + '\n')
            self.channel_logs[channel].flush()

            self.member_logs[sender].write(message + '\n')

    def process(self):
        self.processing = True
        self.identify()

        while self.processing:
            line = self.s.recv(500).rstrip()

            print line

            if len(self.channels) == 0:
                self.join("#dog")

            self.parse_message(line)

    def parse_message(self, line):
        if line[:4] == 'PING':
            parts = line.split()
            if len(parts) > 0 and parts[0] == 'PING':
                self.send('PONG ' + parts[1])

        else:
            whole = line[1:].split(':', 1)
            info = whole[0]
            message = ''
            if len(whole) > 1:
                message = whole[1]
            sender = info.split('!')[0]
            parts = info.split(' ')

            if len(parts) > 1:
                if parts[1] == 'PRIVMSG':
                    channel = parts[2]
                    self.log(channel, sender, message)
                    self.handle_message(channel, sender, message)
                elif parts[1] == 'JOIN':
                    names = message.split('\r\n')
                    channel = names[0]
                    for name in names[1:]:
                        self.parse_message(name)
                    self.member_join(channel, sender)
                elif parts[1] == 'NICK':
                    self.member_nick(sender, message)
                elif parts[1] == 'PART':
                    channel = parts[2]
                    self.member_leave(channel, sender)
                elif parts[1] == 'QUIT':
                    self.member_quit(sender)
                elif len(parts) > 3 and parts[3] == '=':
                    channel = parts[4]
                    members = message.split(' ')[:-1]
                    
                    self.member_names(channel, members)

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

    def member_join(self, channel, member):
        if self.logging:
            self.member_logs[member] = self.open_log('logs/members/', member)
        self.channels[channel].member_join(member)

    def member_leave(self, channel, member):
        if channel in self.channels.keys():
            self.channels[channel].member_leave(member)
        if self.logging and len(self.member_channels(member)) == 0:
            self.member_logs[member].close()
            del self.member_logs[member]

    def member_nick(self, member, nick):
        for key in self.channels.keys():
            self.channels[key].member_nick(member, nick)
        if self.logging:
            self.member_logs[member].close()
            del self.member_logs[member]

            self.member_logs[nick] = self.open_log('logs/members/', nick)

    def member_quit(self, member):
        for key in self.channels.keys():
            self.channels[key].member_leave(member)
        if self.logging:
            self.member_logs[member].close()
            del self.member_logs[member]

    def member_names(self, channel, members):
        for member in members:
            self.member_join(channel, member)

    def member_channels(self, member):
        channels = []
        for key in self.channels.keys():
            if member in self.channels[key].members:
                channels.append(key)

        return channels


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
            clean = self.re_non_punctuation.search(word).group(0)
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
                    new_channel = self.re_channel.search(message).group(0)
                    self.join(new_channel)
                except:
                    pass
            elif has(message, "leave"):
                try:
                    old_channel = self.re_channel.search(message).group(0)
                    self.leave(old_channel)
                except:
                    pass
            elif has(message, "zap"):
                try:
                    tell_channel = self.re_channel.search(message).group(0)
                    self.send_message(tell_channel, statement)
                except:
                    pass
            elif has(message, "topic"):
                topic_channel = channel
                try:
                    topic_channel = self.re_channel.search(message).group(0)
                except:
                    pass
                self.send("TOPIC " + topic_channel + " :" + self.markov.generateN(11))
            elif has(message, "quit"):
                self.quit()
            

