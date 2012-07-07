import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)

# our python app

todoList = []

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", IndexHandler),
			(r"/add", AddHandler)
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static")
		)
		tornado.web.Application.__init__(self, handlers, **settings)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html', list=todoList)
	# def get(self):
	# 	greeting = self.get_argument('greeting', None)
	# 	if greeting:
	# 		self.write(greeting + ', friendly user!')
	# 	else:
	# 		self.write('you got me!')
	# def post(self):
	# 	username = self.get_argument('name', None)
	# 	if username:
	# 		self.write('Nice to meet you, ' + username)
	# 	else:
	# 		self.write('you posted to me!')

class AddHandler(tornado.web.RequestHandler):
	def post(self):
		listitem = self.get_argument('listitem')
		todoList.append(listitem)
		#self.write('OK')
		self.write(str(todoList))

if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(os.environ.get("PORT", 5000))
	tornado.ioloop.IOLoop.instance().start()