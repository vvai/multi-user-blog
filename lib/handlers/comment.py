"""Post related handlers."""
from blog_handler import BlogHandler
from google.appengine.ext import db
from lib.db.comment import Comment


class NewComment(BlogHandler):
    """New comment handler."""

    def get(self, post_id):
        """Get request."""
        if self.user:
            self.render("newcomment.html")
        else:
            return self.redirect("/login")

    def post(self, post_id):
        """Post request."""
        if not self.user:
            return self.redirect('/login')

        comment = self.request.get('comment')
        user_id = self.read_secure_cookie('user_id')

        if comment:
            c = Comment(parent=self.blog_key(),
                        content=comment,
                        user_id=user_id,
                        post_id=post_id)
            c.put()
            return self.redirect('/blog/%s' % str(post_id))
        else:
            error = "write your comment, please!"
            self.render("newcomment.html",
                        error=error)


class EditComment(BlogHandler):
    """Edit comment handler."""

    def get(self, post_id, comment_id):
        """Get request."""
        if self.user:
            key = db.Key.from_path('Post',
                                   int(post_id),
                                   parent=self.blog_key())
            post = db.get(key)
            comment_key = db.Key.from_path('Comment',
                                           int(comment_id),
                                           parent=self.blog_key())
            comment = db.get(comment_key)
            user_id = self.read_secure_cookie('user_id')
            if not (post and comment):
                self.error(404)
                return
            if comment.user_id == user_id:
                self.render("newcomment.html",
                            comment=comment.content,
                            comment_id=comment_id,
                            error="")
            else:
                return self.redirect('/blog/%s' % str(post_id))

        else:
            return self.redirect("/login")

    def post(self, post_id, comment_id):
        """Edit comment request."""
        if not self.user:
            return self.redirect('/login')

        comment = self.request.get('comment')
        user_id = self.read_secure_cookie('user_id')

        key = db.Key.from_path('Comment',
                               int(comment_id),
                               parent=self.blog_key())
        c = db.get(key)
        if c.user_id != user_id:
            return self.redirect("/login")
        if comment:
            c.content = comment
            c.put()
            return self.redirect('/blog/%s' % str(post_id))
        else:
            return self.redirect('/blog/%s' % str(post_id))


class DeleteComment(BlogHandler):
    """Delete comment handler."""

    def get(self, post_id, comment_id):
        """Delete comment request."""
        if not self.user:
            return self.redirect('/login')

        key = db.Key.from_path('Comment',
                               int(comment_id),
                               parent=self.blog_key())
        comment = db.get(key)
        user_id = self.read_secure_cookie('user_id')

        if comment:
            if comment.user_id == user_id:
                comment.delete()
                return self.redirect('/blog/%s' % str(post_id))
            else:
                return self.redirect('/blog/%s' % str(post_id))
        else:
            return self.redirect('/blog/%s' % str(post_id))
