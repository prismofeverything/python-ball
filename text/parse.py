import re
import utility

spuriousNewlines = re.compile("\r\n")
deperiodTitle = re.compile("(Mrs?)\.")
inBrackets = re.compile("\[[^\]]*\]")

def parseConversation(string):
    lines = string.split("\n")
    groups = [line.split() for line in lines]

    return groups

def parseBook(string):
    straight = spuriousNewlines.sub(' ', string)
    normal = deperiodTitle.sub(r"\1", straight)
    lines = normal.split(".")
    lines = [line + '.' for line in lines]
    groups = [line.split() for line in lines]

    return groups
    
def markovText(text):
    conversation = parseConversation(text)

    chain = utility.MarkovChain()
    chain.appendSource(conversation)

    return chain

def markovBook(name):
    file = open(name)
    book = file.read()
    book = parseBook(book)

    chain = utility.MarkovChain()
    chain.appendSource(book)
    file.close()

    return chain
