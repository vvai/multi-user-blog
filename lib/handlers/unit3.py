"""Unit 3 handlers."""
from blog_handler import BlogHandler
from signup import Signup
from lib.db.user import User
from lib.db.post import Post
from lib.db.comment import Comment


class Register(Signup):
    """Register handler."""

    def done(self):
        """Override done method."""
        # make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/blog')


class Login(BlogHandler):
    """Login handler."""

    def get(self):
        """Get request."""
        self.render('login-form.html')

    def post(self):
        """Post request."""
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)


class Logout(BlogHandler):
    """Logout handler."""

    def get(self):
        """Get request."""
        self.logout()
        self.redirect('/blog')


class Unit3Welcome(BlogHandler):
    """Welcome request."""

    def get(self):
        """Get request."""
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/signup')


class BlogFront(BlogHandler):
    """Blog front page handler."""

    def get(self):
        """Get request."""
        posts = Post.all().order('-created')
        self.render('front.html', posts=posts)
