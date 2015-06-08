import os
import re
from string import letters
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
        
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(BlogHandler):
    # def render_front(self, title="", art="", error=""):
        # arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        # #arts = top_arts()
        # #points = []
        # #for a in arts:
        # #    if a.coords:
        # #        points.append(a.coords)
        
        # #img_url = None
        # #if points:
        # #    img_url = gmaps_img(points)
        
        # self.render("front.html", title=title, art=art, error = error, arts = arts)
        
    def get(self):
        #self.render_front()
        self.write("Hello, Uda!")
        
    # def post(self):
        # title = self.request.get("title")
        # art = self.request.get("art")
        # if title and art:
            # #coords = get_coords(self.request.remote_addr)
            # a = Art(title = title, art = art)
            # #if coords:
            # #    a.coords = coords
            # a.put()
            # #top_arts(True)
            
            # self.redirect("/")
        # else:
            # error = "we need both a title and some artwork!"
            # self.render_front(title, art, error)

# blog stuff            
            
def blog_key(name="default")"
    return db.Key.from_path('blogs', name)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
    def render(self):
        self.render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)
        
class BlogFront(BlogHandler):
    def get(self):
        posts = greetins = Post.all().order('-created')
        self.render.('front.html', posts = posts)
        
class PostPage(BlogHandler):
    def get(self, post_id):
        key = виюЛунюакщь_зфер(
        
    
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)