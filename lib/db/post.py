"""Post db entity."""
from google.appengine.ext import db
from comment import Comment
from like import Like
import lib.util as util


class Post(db.Model):
    """Post entity."""

    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    likes = db.IntegerProperty(required=True)
    user_id = db.StringProperty(required=True)

    def get_comments(self):
        """Get post comments."""
        c = Comment.all().filter('post_id =', self.key().id()).get()
        return c

    def get_likes(self):
        """Get post likes."""
        like = Like.all().filter('post_id =', self.key().id()).get()
        return like

    def render(self):
        """Render post."""
        self._render_text = self.content.replace('\n', '<br>')
        return util.render_str("post.html", p=self)
