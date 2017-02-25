"""module contains base class for all handlers."""
import webapp2
import lib.util as util
from google.appengine.ext import db
from lib.db.user import User


class BlogHandler(webapp2.RequestHandler):
    """base class for all handlers."""

    def write(self, *a, **kw):
        """Write response to user."""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """Render string."""
        params['user'] = self.user
        return util.render_str(template, **params)

    def render(self, template, **kw):
        """Render."""
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        """Set cookie."""
        cookie_val = util.make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        """Read cookie."""
        cookie_val = self.request.cookies.get(name)
        return cookie_val and util.check_secure_val(cookie_val)

    def login(self, user):
        """Login."""
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        """Logout."""
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        """Initialize."""
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

    def blog_key(self, name='default'):
        """Get key."""
        return db.Key.from_path('blogs', name)
