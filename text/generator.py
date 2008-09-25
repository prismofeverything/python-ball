import comments
import parse
import utility

class MarkovGenerator():
    def __init__(self):
        self.comments = comments.CommentExtractor()

    def generate(self, id):
        chain = utility.MarkovChain()
        comments = self.comments.get_comments(id)
        parsed = parse.parseRedditComments(comments)

        chain.appendSource(parsed)

        return chain
