import web
import zarathustra

Z = zarathustra.Zarathustrabot()

render = web.template.render('templates/',cache=False)

urls = (
    '/', 'home',
    '/blog', 'blog'
)

class home:
    def GET(self):
        web.header('Content-Type', 'text/html')
        output = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
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
      <p>""" + Z.generate() + """</p>
    </div>
  </body>
</html>"""

        print(output)

web.webapi.internalerror = web.debugerror

if __name__ == "__main__": 
    web.run(urls, globals(), web.reloader)

