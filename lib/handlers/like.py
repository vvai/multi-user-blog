"""Like related handlers."""
from blog_handler import BlogHandler
from google.appengine.ext import db
from lib.db.like import Like


class LikePost(BlogHandler):
    """Like post handler."""

    def get(self, post_id):
        """Like post request."""
        if not self.user:
            return self.redirect('/login')

        user_id = self.read_secure_cookie('user_id')
        like = (
                    Like.all()
                    .filter('post_id =', post_id)
                    .filter('user_id =', user_id)
                    .fetch(1)
                )

        if post_id and user_id and not like:
            like = Like(parent=self.blog_key(),
                        user_id=user_id,
                        post_id=post_id)
            like.put()
            return self.redirect('/blog/%s' % str(post_id))
        else:
            return self.redirect('/blog')


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
                return self.redirect('/blog/%s' % str(post_id))
        else:
            return self.redirect('/login')
