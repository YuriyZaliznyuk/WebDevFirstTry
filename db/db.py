import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

hidden_html ="""
<input type="hidden" name="food" value="%s">
"""

item_html = "<li>%s</li>"

shopping_list_html = """
<br>
<br>
<h2>Shopping List</h2>
<ul>
%s
</ul>
"""

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
		
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))		
		
class MainPage(Handler):
    def get(self):
        n = self.request.get("n")
        if n:
            n = int(n)
        self.render("shopping_list.html", n=n)
        
class FizzBuzz(Handler):
    def get(self):
        n = self.request.get("n")
        if n.isdigit():
            n = int(n)
        self.render("fizzbuzz.html", n = n)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/fizzbuzz', FizzBuzz),
                              ], debug=True)