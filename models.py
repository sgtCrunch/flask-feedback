"""Models for feedback"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users Model"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        print(email)
        hashed = bcrypt.generate_password_hash(password)
        hashed_utc = hashed.decode("utf8")

        return cls(username=username, password=hashed_utc, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, password):

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    
class Feedback(db.Model):
    """Feedback Model"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), db.ForeignKey('users.username'))

    user = db.relationship("User", backref= backref("feedback", cascade="all,delete"))
