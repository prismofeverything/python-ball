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



# class blips:
#     def GET(self):
#         try:
#             source_id = web.input().source_id
#         except AttributeError:
#             print('No source found')
#             return
#         query = """select blips.url, 
#                    referrals.date,
#                    referrals.hits 
#                    from blips
#                    left join referrals on blips.id = referrals.blip_id 
#                    where referrals.hits is not NULL
#                    and blips.source_id = %s """ % (web.sqlquote(source_id))
#         try:
#             date_from = web.input().date_from
#             date_to = web.input().date_to
#             query +=  ' and referrals.date between %s and %s' % (web.sqlquote(date_from), web.sqlquote(date_to))
#         except AttributeError:
#             pass
#         query += ' order by referrals.date desc'
#         output = utils.render_json(web.query(query))
#         web.header('Content-Type', 'application/json')
#         print(output)

# class sources:
#     def GET(self):
#         query = """select sum(referrals.hits) as count, 
#                    sources.id, 
#                    sources.domain, 
#                    sources.name,
#                    sources.topic
#                    from sources, blips, referrals 
#                    where sources.topic is not null and
#                    blips.source_id = sources.id and 
#                    referrals.blip_id = blips.id """
#         try:
#             date_from = web.input().date_from
#             date_to = web.input().date_to
#             query +=  ' and referrals.date between %s and %s' % (web.sqlquote(date_from), web.sqlquote(date_to))
#         except AttributeError:
#             pass
#         query += ' group by sources.domain order by count desc'
#         output = web.query(query)
#         try:
#             detail = web.input().detail
#             detail_query = """select sum(hits) as count, 
#                               referrals.date 
#                               from referrals, blips 
#                               where referrals.blip_id = blips.id and 
#                               blips.source_id = %s 
#                               group by date order by date desc"""
#             new_output = []
#             for i in output:
#                 res = web.query(detail_query % (i.id))
#                 i.detail = res
#                 new_output.append(i)
#             web.header('Content-Type', 'application/json')
#             print(utils.render_json(new_output))

#         except AttributeError:
#             web.header('Content-Type', 'application/json')
#             print utils.render_json(output)

# class demo:
#     def GET(self):
#         print render.demo()

