import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class Rot13(BaseHandler):
    def get(self):
        self.render('rot13-form.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('rot13-form.html', text = rot13)

    # note that python uses elif, not else if
    def encode(self, str_in):
        mylist = []
        for i in str_in:
            x = ord(i)
            if x >= 65 and x <= 77:
                mylist.append(chr(x + 13))
            elif x >= 78 and x <= 90:
                mylist.append(chr(x - 13))
            elif x >= 97 and x <= 109:
                mylist.append(chr(x + 13))
            elif x >= 110 and x <= 122:
                mylist.append(chr(x - 13))
            elif x==32:
                mylist.append(chr(x))
            else: 
                print "You have inserted an invalid character."

        newstring = ''.join(mylist)
        return newstring

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")


def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_email(email):
    return not email or EMAIL_RE.match(email)

app = webapp2.WSGIApplication([
    ('/', Rot13)
], debug=True)
