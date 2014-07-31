
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Thesis(ndb.Model):
	title=ndb.StringProperty(indexed=False)
	author=ndb.StringProperty(indexed=False)
	year=ndb.StringProperty(indexed=False)
	status=ndb.StringProperty(indexed=False)
	description=ndb.StringProperty(indexed=False)

class SuccessPageHandler(webapp2.RequestHandler):
    def get(self):
		template = JINJA_ENVIRONMENT.get_template('success.html')
 		self.response.write(template.render())

class ThesisNewHandler(webapp2.RequestHandler):
    def get(self):
		template = JINJA_ENVIRONMENT.get_template('thesis_new.html')
 		self.response.write(template.render())

    def post(self):
 		thesis = Thesis() 
		thesis.title = self.request.get('title')
		thesis.author= self.request.get('author')
		thesis.year = self.request.get('year')
		thesis.status = self.request.get('status')
		thesis.description = self.request.get('description')
 		thesis.put()
 		self.redirect('/success')

class ThesisDescriptionHandler(webapp2.RequestHandler):
        def get(self, thesis_id):
                thesis_all=Thesis.query().fetch()
                thesis_id = int(thesis_id)
                template_values={
                        'id': thesis_id,
                        'thesis_all': thesis_all
                }
                template = JINJA_ENVIRONMENT.get_template('thesis_description.html')
                self.response.write(template.render(template_values))
 
class ThesisListHandler(webapp2.RequestHandler):
        def get(self):
                thesis_all=Thesis.query().fetch()
                template_values={
                        'thesis_all': thesis_all
                }
 
                template = JINJA_ENVIRONMENT.get_template('thesis_list.html')
                self.response.write(template.render(template_values))
		

app = webapp2.WSGIApplication([
	('/thesis/new', ThesisNewHandler),
	('/success', SuccessPageHandler),
	('/thesis/list', ThesisListHandler),
	('/thesis/description/(\d+)', ThesisDescriptionHandler)
], debug=True)
