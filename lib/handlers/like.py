"""Like related handlers."""
from blog_handler import BlogHandler
from google.appengine.ext import db
from lib.db.like import Like


class LikePost(BlogHandler):
    """Like post handler."""

    def get(self, post_id):
        """Like post request."""
        if not self.user:
            self.redirect('/blog')

        user_id = self.read_secure_cookie('user_id')

        if post_id and user_id:
            like = Like(parent=self.blog_key(),
                        user_id=user_id,
                        post_id=post_id)
            like.put()
            self.redirect('/blog/%s' % str(post_id))
        else:
            self.redirect('/blog')


class DislikePost(BlogHandler):
    """Disike post handler."""

    def get(self, post_id, like_id):
        """Dislike post request."""
        if self.user:
            key = db.Key.from_path('Like',
                                   int(like_id),
                                   parent=self.blog_key())
            like = db.get(key)
            if like:
                like.delete()
                self.redirect('/blog/%s' % str(post_id))
        else:
            self.redirect('/blog')
