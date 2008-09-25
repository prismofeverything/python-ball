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
    
def markovBook(name):
    book = open(name).read()
    book = parseBook(book)
    chain = utility.MarkovChain()
    chain.appendSource(book)

    return chain
