import cherrypy
import json
import pickle
import os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))


class Root:
	def __init__(self):
		if os.path.isfile("config.json"):
			f = open("config.json", "rb")
			self.config = pickle.load(f)
		else:
			self.config = []

	@cherrypy.expose
	def index(self):
		tmpl = env.get_template('index.html')
		return tmpl.render(initial_json=json.dumps(self.config))

	@cherrypy.expose
	def configuration(self):
		tmpl = env.get_template('configuration.html')
		return tmpl.render(initial_json=json.dumps(self.config))

	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	def update_answer(self):
		j = cherrypy.request.json
		return "{OK}"

	@cherrypy.expose
	@cherrypy.tools.json_out()
	def send_config(self): #TODO do this.
		return json.dumps(self.config)

	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	def receive_config(self): #TODO do this too
		j = cherrypy.request.json
		self.config = j
		f = open("config.json", "wb")
		pickle.dump(self.config, f)
		return json.dumps(["OK"])




cherrypy.quickstart(Root(), "/", config={
		'global':{'server.socket_host': '127.0.0.1',
					'server.socket_port': 8080
		 },
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
        '/css':{ 'tools.staticdir.on':True,
          'tools.staticdir.dir':"templates/css"
        },
		'/js':{'tools.staticdir.on': True,
		 'tools.staticdir.dir': "templates/js"
		}

})