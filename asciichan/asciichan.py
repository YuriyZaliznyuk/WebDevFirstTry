import os
import webapp2
import jinja2
import urllib2
from xml.dom import minidom
from string import letters

from google.appengine.ext import db
from google.appengine.api import memcache

DEBUG = os.environ('SERVER_SOFTWARE').startswith('Development')

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),                                    autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
    ip = "" # For testing
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLerror:
        return
    
    if content:
        d = minidom.parseString(content)
        coord = d.getElementsByTagName('gml:coordinates')
        if coord and coord[0].childNodes[0].nodeValue:
            lon, lat = coord[0].childNodes[0].nodeValue.split(',')
            return db.GeoPt(lat, lon)

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
def gmaps_img(points):
    markers = '&'.join("markers=%s,%s" % (p.lat, p.lon) for p in points)
    return GMAPS_URL + markers
        
class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    coords = db.GeoPtProperty()

def top_arts(update = False):
    key = 'top'
    arts = memcache.get(key)
    if arts is None or update:
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC limit 10")
        # to prevent from running multiple queries
        arts = list(arts)
        memcache.set(key, arts)
    return arts
    
class MainPage(Handler):
    def render_front(self, title="", art="", error=""):
        
        arts = top_arts()
        points = []
        for a in arts:
            if a.coords:
                points.append(a.coords)
        #alternate implementation of the above for loop:
        #points = filter(None, (a.coords for a in arts)
        
        img_url = None
        if points:
            img_url = gmaps_img(points)
        
        #alternative:
        # points = filter(None, (a.coords for a in arts))
        self.render("front.html", title=title, art=art, error = error, arts = arts, img_url = img_url)
        
    def get(self):
        self.render_front()
        
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        if title and art:
            coords = get_coords(self.request.remote_addr)
            a = Art(title = title, art = art)
            if coords:
                a.coords = coords
            a.put()
            #CACHE.clear()
            # rerun the query and update the cache
            top_arts(True)
            
            self.redirect("/")
        else:
            error = "we need both a title and some artwork!"
            self.render_front(title, art, error)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)