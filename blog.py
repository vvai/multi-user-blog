"""Main script."""
# C:\sp\google-cloud-kit\google-cloud-sdk\bin\dev_appserver.py
# --clear_datastore --port=3000 .
# gcloud app deploy
import webapp2
from lib.handlers.blog_handler import BlogHandler
from lib.handlers.unit2 import Welcome, Unit2Signup, Rot13
from lib.handlers.unit3 import BlogFront, Register, Login, Logout, Unit3Welcome
from lib.handlers.post import PostPage, NewPost, EditPost, DeletePost
from lib.handlers.comment import NewComment, EditComment, DeleteComment
from lib.handlers.like import LikePost, DislikePost


# def render_post(response, post):
#    response.out.write('<b>' + post.subject + '</b><br>')
#    response.out.write(post.content)


class MainPage(BlogHandler):
    """Main page handler."""

    def get(self):
        """Get request."""
        self.write('Hello, Udacity!')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/unit2/rot13', Rot13),
                               ('/unit2/signup', Unit2Signup),
                               ('/unit2/welcome', Welcome),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/blog/editpost/([0-9]+)', EditPost),
                               ('/blog/deletepost/([0-9]+)', DeletePost),
                               ('/blog/([0-9]+)/newcomment', NewComment),
                               ('/blog/([0-9]+)/editcomment/([0-9]+)',
                               EditComment),
                               ('/blog/([0-9]+)/deletecomment/([0-9]+)',
                               DeleteComment),
                               ('/blog/([0-9]+)/like', LikePost),
                               ('/blog/([0-9]+)/dislike/([0-9]+)',
                               DislikePost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/unit3/welcome', Unit3Welcome),
                               ],
                              debug=True)
