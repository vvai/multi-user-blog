"""Post related handlers."""
from blog_handler import BlogHandler
from google.appengine.ext import db
from lib.db.post import Post
from lib.db.comment import Comment
from lib.db.like import Like


class PostPage(BlogHandler):
    """Post page handler."""

    def get(self, post_id):
        """Get request."""
        user_id = self.read_secure_cookie('user_id')
        post, comments, like, likes_count = getPostInformation(self.blog_key(),
                                                               post_id,
                                                               user_id)
        if not post:
            self.error(404)
            return self.redirect('error.html')

        self.render("permalink.html",
                    post=post,
                    comments=comments,
                    like=like,
                    likes_count=likes_count,
                    user_id=user_id)


class NewPost(BlogHandler):
    """New post handler."""

    def get(self):
        """Get request."""
        if self.user:
            self.render("newpost.html")
        else:
            return self.redirect("/login")

    def post(self):
        """Post request."""
        if not self.user:
            return self.redirect('/login')

        subject = self.request.get('subject')
        content = self.request.get('content')
        user_id = self.read_secure_cookie('user_id')

        if subject and content:
            p = Post(parent=self.blog_key(),
                     subject=subject,
                     content=content,
                     user_id=user_id,
                     likes=0)
            p.put()
            return self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html",
                        subject=subject,
                        content=content,
                        error=error)


class EditPost(BlogHandler):
    """Edit post handler."""

    def get(self, post_id):
        """Get request."""
        if self.user:
            user_id = self.read_secure_cookie('user_id')
            post, comments, like, likes_count = getPostInformation(
                                                      self.blog_key(),
                                                      post_id,
                                                      user_id)
            if not post:
                self.error(404)
                return
            if post.user_id == user_id:
                self.render("newpost.html",
                            subject=post.subject,
                            content=post.content,
                            error="")
            else:
                error = "This is not your post, you cannot edit or delete it."
                self.render("permalink.html",
                            post=post,
                            comments=comments,
                            like=like,
                            likes_count=likes_count,
                            user_id=user_id,
                            error=error)

        else:
            return self.redirect("/login")

    def post(self, post_id):
        """Edit post request."""
        if not self.user:
            return self.redirect('/login')

        subject = self.request.get('subject')
        content = self.request.get('content')

        key = db.Key.from_path('Post', int(post_id), parent=self.blog_key())
        post = db.get(key)

        if subject and content and post:
            post.subject = subject
            post.content = content
            post.put()
            return self.redirect('/blog/%s' % str(post.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html",
                        subject=subject,
                        content=content,
                        error=error)


class DeletePost(BlogHandler):
    """Delete post handler."""

    def get(self, post_id):
        """Delete post request."""
        if not self.user:
            self.redirect('/login')

        user_id = self.read_secure_cookie('user_id')
        post, comments, like, likes_count = getPostInformation(self.blog_key(),
                                                               post_id,
                                                               user_id)
        if post:
            if post.user_id == user_id:
                post.delete()
                self.redirect('/blog')
            else:
                error = "This is not your post, you cannot edit or delete it."
                self.render("permalink.html",
                            post=post,
                            comments=comments,
                            like=like,
                            likes_count=likes_count,
                            user_id=user_id,
                            error=error)
        else:
            # error = "this is not yours post"
            return self.redirect('/blog/%s' % str(post.key().id()))


def getPostInformation(blog_key, post_id, user_id):
    """Get post id."""
    key = db.Key.from_path('Post', int(post_id), parent=blog_key)
    post = db.get(key)
    comments = Comment.all().filter('post_id =', post_id).fetch(None)
    like = (
                Like.all()
                .filter('post_id =', post_id)
                .filter('user_id =', user_id)
                .fetch(1)
            )
    likes_count = len(
                        Like.all()
                        .filter('post_id =', post_id)
                        .fetch(None)
                     )
    return (post, comments, next(iter(like or []), None), likes_count)
