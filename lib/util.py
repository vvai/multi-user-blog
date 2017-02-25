"""Util variables and functions."""
import jinja2
import os
import hmac
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def render_str(template, **params):
    """Render string."""
    t = jinja_env.get_template(template)
    return t.render(params)


secret = 'fart'


def make_secure_val(val):
    """Make secure value."""
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    """Check secure value."""
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


def valid_username(username):
    """Check username validity."""
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username and USER_RE.match(username)


def valid_password(password):
    """Check password validity."""
    PASS_RE = re.compile(r"^.{3,20}$")
    return password and PASS_RE.match(password)


def valid_email(email):
    """Check email validity."""
    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    return not email or EMAIL_RE.match(email)
