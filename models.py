
from google.appengine.ext import db

class Person(db.Model):
    openid = db.LinkProperty(verbose_name="OpenID")

class Piece(db.Model):
    creator = db.ReferenceProperty(Person)
    x       = db.IntegerProperty()
    y       = db.IntegerProperty()
    icon    = db.StringProperty()
    name    = db.StringProperty()
    desc    = db.TextProperty()
