#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api.datastore_errors import BadValueError
import django.utils.simplejson as json

class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            obj = dict(obj)
        return super(ModelEncoder, self).default(obj)


class Person(db.Model):
    openid = db.LinkProperty(verbose_name="OpenID")

class Piece(db.Model):
    creator = db.ReferenceProperty(Person)
    x       = db.IntegerProperty()
    y       = db.IntegerProperty()
    icon    = db.StringProperty()
    name    = db.StringProperty()
    desc    = db.TextProperty()


class Handlr(webapp.RequestHandler):
    def json(self, data):
        self.response.out.write(json.dumps(data, cls=ModelEncoder))
    def render(self, tmpl, data=None, **kwargs):
        if data is None:
            data = {}
        if kwargs:
            data.update(kwargs)    
        self.response.out.write(template.render('templates/' + tmpl + '.html', data))

class MainHandler(Handlr):
    def get(self):
        self.render('main', msg="Hello world!")

class StuffHandler(Handlr):
    def get(self):
        stuff = Piece.all().fetch()
        stuff_data = [dict(x) for x in stuff]
        self.response.out.write('CANHAZ ' + json.dumps(stuff_data))

urlmap = (
    ('/', StuffHandler),
)

def main():
    application = webapp.WSGIApplication(urlmap, debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
