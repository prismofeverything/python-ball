import web
import zarathustra

Z = zarathustra.Zarathustrabot()

render = web.template.render('templates/',cache=False)

urls = (
    '/?', 'home',
    '/(\d+)/?', 'number',
    '/(\w+)/?', 'word'
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
      <p>ZARATHUSTRA SAYS:</p>
    </div>
    <div id="statement">
      <p>""" + statement + """</p>
    </div>
  </body>
</html>"""

class home:
    def GET(self):
        web.header('Content-Type', 'text/html')
        output = render_statement(Z.generate())

        print(output)

class number:
    def GET(self, n):
        web.header('Content-Type', 'text/html')
        if n > 33333:
            n = 33333
        output = render_statement(Z.markov.generateN(int(n)))

        print(output)

class word:
    def GET(self, word):
        web.header('Content-Type', 'text/html')

        if Z.markov.has(word):
            statement = Z.markov.expandFrom(word)
        else:
            statement = 'I do not know ' + word + '.'

        output = render_statement(statement)
        print(output)
    

web.webapi.internalerror = web.debugerror

if __name__ == "__main__": 
    web.run(urls, globals(), web.reloader)

