import webapp2
import jinja2
import re
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class SignUp(Handler):
    def get(self):

        self.render("sign_up_mainpage")

    def post(self):
        have_error = False
        users_username = self.request.get('username')
        user_email = self.request.get('email')
        verify = self.request.get('verify')
        good_pass_question_mark = self.request.get('password')

        params = dict(username = users_username, email = user_email)

        if not valid_username(users_username):
            params['UNerror'] = "Not a valid username"
            have_error = True

        if not valid_password(good_pass_question_mark):
            params['PWerror'] = "Not a valid password"
            have_error = True

        elif good_pass_question_mark != verify:
            params['PWdontmatcherror'] = "Your passwords did not match"
            have_error = True

        if not valid_email(user_email):
            params['EMAILerror'] = "Not a valid e-mail, friend"
            have_error = True

        if have_error:
            self.render("sign_up_mainpage", **params)

        else:
            self.redirect("/welcome?username=" + users_username)

class WelcomePage(Handler):

    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', barkley = username)
        

app = webapp2.WSGIApplication([
    ('/', SignUp),
    ('/welcome', WelcomePage)], debug=True)
