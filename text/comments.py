import urllib
from sgmllib import SGMLParser

def get_page(url):
    f = urllib.urlopen(url)
    s = f.read()

    return s

class CommentExtractor(SGMLParser):
    def __init__(self, verbose=0):
        SGMLParser.__init__(self, verbose)

        self.id = None
        self.comments = []

        self.in_comment = 0
        self.starting_comment = 0

    def reset(self):
        SGMLParser.reset(self)

    def start_div(self, attrs):
        for (key, value) in attrs:
            if key == 'class' and value == 'commentbody':
                self.in_comment = 1
                self.starting_comment = 1

    def end_div(self):
        self.in_comment = 0
        self.starting_comment = 0

    def handle_data(self, data):
        if self.in_comment:
            if self.starting_comment:
                self.comments.append(data)
                self.starting_comment = 0
            else:
                self.comments[-1] += data


    def get_comments(self, id):
        self.comments = []
        comments_left = True
        base_address = "http://reddit.com/user/"+id+"/?offset="
        page_index = 0

        while comments_left and page_index < 40:
            page=get_page(base_address + str(25 * page_index))

            if page.find("there are no results here") >= 0:
                comments_left = False
            else:
                self.feed(page)
                page_index += 1

            print page_index * 25

        return self.comments

    def write_comments(self, id):
        comments = self.get_comments(id)
        f = open(id, 'w')

        for comment in comments:
            f.write(comment)

        f.close()

