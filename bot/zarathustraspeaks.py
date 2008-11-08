import web
import zarathustra

Z = zarathustra.Zarathustrabot()

render = web.template.render('templates/',cache=False)

urls = (
    '/?', 'home',
    '/(\d+)/?', 'number',
    '/([^/]*)/?', 'word'
)

def render_statement(statement):
    return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>Zarathustra SPEAKS</title>
    <link rel="stylesheet" href="/static/app.css" type="text/css" />
  </head>
  <body>
    <div id="speaks">
      <p><a href="/" class="title">ZARATHUSTRA SAYS:</a></p>
    </div>
    <div id="statement">
      <p>""" + statement + """</p>
    </div>
  </body>
</html>"""


def anchorize_word(word):
    return '<a href="/' + word + '/" class="word">' + word + '</a>'

def anchorize_statement(statement):
    words = statement.split(' ')
    anchors = [anchorize_word(word) for word in words]

    return ' '.join(anchors)

class home:
    def GET(self):
        web.header('Content-Type', 'text/html')
        output = render_statement(anchorize_statement(Z.generate()))

        print(output)

class number:
    def GET(self, n):
        web.header('Content-Type', 'text/html')
        if n > 33333:
            n = 33333
        statement = Z.markov.generateN(int(n))
        output = render_statement(anchorize_statement(statement))

        print(output)

class word:
    def GET(self, word):
        web.header('Content-Type', 'text/html')

        if Z.markov.has(word):
            statement = Z.markov.expandFrom(word)
        else:
            statement = 'I do not know ' + word + '.'

        output = render_statement(anchorize_statement(statement))
        print(output)
    

web.webapi.internalerror = web.debugerror

if __name__ == "__main__": 
    web.run(urls, globals(), web.reloader)

