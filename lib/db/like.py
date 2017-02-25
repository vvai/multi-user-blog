"""Like db entity."""
from google.appengine.ext import db


class Like(db.Model):
    """Like entity."""

    user_id = db.StringProperty(required=True)
    post_id = db.StringProperty(required=True)
