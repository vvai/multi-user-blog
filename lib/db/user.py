"""User db entity."""
import hashlib
import random
from string import letters
from google.appengine.ext import db


class User(db.Model):
    """User class."""

    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        """Get user by id."""
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        """Get user by name."""
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        """Register user."""
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        """Login."""
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


def make_pw_hash(name, pw, salt=None):
    """Make password hash."""
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def users_key(group='default'):
    """Get users key."""
    return db.Key.from_path('users', group)


def valid_pw(name, password, h):
    """Check password validity."""
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


def make_salt(length=5):
    """Make salt."""
    return ''.join(random.choice(letters) for x in range(length))
