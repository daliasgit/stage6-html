import os
import jinja2
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

# Set up jinja environment
template_dir = os.path.join(os.path.dirname ('base.html'), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), extensions = ['jinja2.ext.autoescape'], autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#Creating modify page object by defining class. 
class ModifyPage(ndb.Model):
      comment = ndb.StringProperty(indexed=False)
      date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):
    def get(self):
        #added this for triggering error
        error=self.request.get('error'," ")
        #instantiates another object used for pulling and displaying comments.
        query = ModifyPage.query().order(ModifyPage.date)
        info_list = query.fetch()
        self.render("index.html", comment=info_list, error=error)

    def post(self):
        #pull a reference object to ModifyPage object to pull the objects from Google Datastore. Queries all objects in database.Use fetch
        #to limit query to specified number.
        pull_posts = 5
        query = ModifyPage.query()
        page_comments = query.fetch(pull_posts)
        print page_comments

        #added per nitpick from 1st review to test code
        #logging.debug("your message")
        comment = self.request.get('comment')
        #writes object to Google Datastore server               
        #using comment.strip() to trigger error when only spaces entered.            
        if comment.strip():
            modify_page = ModifyPage(comment=comment)
            modify_page.content=self.request.get('comment')
            modify_page.put()
            import time
            delay = 00.1
            time.sleep(delay)
            self.redirect('/')

        else:
             self.redirect('/?error = Please fill out comment section!')

app = webapp2.WSGIApplication ([('/', MainPage), ],debug=True)

