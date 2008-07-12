#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Handlr(webapp.RequestHandler):
    def render(self, tmpl, data=None, **kwargs):
        if data is None:
            data = {}
        if kwargs:
            data.update(kwargs)    
        self.response.out.write(template.render('templates/' + tmpl + '.html', data))

class MainHandler(Handlr):
    def get(self):
        self.render('main', { 'msg': "Hello world!" })


urlmap = (
    ('/', MainHandler),
    
    ('/dev', MainHandler),
)

def main():
    application = webapp.WSGIApplication(urlmap, debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
