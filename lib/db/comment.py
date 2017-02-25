"""Comment db entity."""
from google.appengine.ext import db
import lib.util as util


class Comment(db.Model):
    """Comment entity."""

    user_id = db.StringProperty(required=True)
    post_id = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    def render(self, user_id):
        """Render comment."""
        self._render_text = self.content.replace('\n', '<br>')
        return util.render_str("comment.html", c=self, user_id=user_id)
