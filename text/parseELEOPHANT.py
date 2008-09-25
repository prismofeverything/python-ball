def parseConversation(string):
    lines = string.split("\n")
    groups = [line.split() for line in lines]

    return groups

def parseRedditComments(comments):
    groups = [line.split() for line in comments]
    return groups
