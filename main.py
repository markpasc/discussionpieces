#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api.datastore_errors import BadValueError
import django.utils.simplejson as json

from models import *

class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            jobj = dict([(k, getattr(obj, k, None)) for k in obj.properties().keys()])
            jobj['key'] = str(obj.key())
            return jobj
        elif isinstance(obj, db.Property):
            return str(obj)
        return super(ModelEncoder, self).default(obj)

class Handlr(webapp.RequestHandler):
    def json(self, data):
        self.response.out.write(json.dumps(data, cls=ModelEncoder))
    def render(self, tmpl, data=None, **kwargs):
        if data is None:
            data = {}
        if kwargs:
            data.update(kwargs)    
        self.response.out.write(template.render('templates/' + tmpl + '.html', data))
    def oops404(self, msg=None):
        self.response.set_status(404)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(msg if msg else 'Not found')

class MainHandler(Handlr):
    def get(self):
        self.render('main', msg="Hello world!", icons=ICONS)

class StuffHandler(Handlr):
    def get(self, key=None):
        stuff = Piece.all()
        stuff_data = stuff.fetch(10)
        self.json(stuff_data)
    def post(self, key=None):
        if key:
            p = Piece.get(key)
            if not p:
                self.oops404('No such piece')
                return
        else:
            p = Piece()
            (p.creator,) = Person.all().fetch(1)
            p.icon = self.request.get('icon')
            p.name = self.request.get('name')
            p.desc = self.request.get('desc')
        (p.x, p.y) = [int(self.request.get(m)) for m in ('x', 'y')]
        p.save()
        self.json(p)

urlmap = (
    (r'/stuff(?:/(?P<key>\w+))?', StuffHandler),
    (r'/', MainHandler),
)

def main():
    application = webapp.WSGIApplication(urlmap, debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
