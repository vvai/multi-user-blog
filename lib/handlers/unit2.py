"""handlers from unit2."""
from blog_handler import BlogHandler
import lib.util as util
from signup import Signup


class Welcome(BlogHandler):
    """Welcome page handler."""

    def get(self):
        """Get request."""
        username = self.request.get('username')
        if util.valid_username(username):
            self.render('welcome.html', username=username)
        else:
            self.redirect('/unit2/signup')


class Rot13(BlogHandler):
    """Rot13 handler."""

    def get(self):
        """Get request."""
        self.render('rot13-form.html')

    def post(self):
        """Post request."""
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')
        self.render('rot13-form.html', text=rot13)


class Unit2Signup(Signup):
    """Signup handler."""

    def done(self):
        """Redirect to welcome page."""
        self.redirect('/unit2/welcome?username=' + self.username)
