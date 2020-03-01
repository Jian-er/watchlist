import datetime
from project import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def __str__(self):
        return User.name

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Ariticles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    content = db.Column(db.Text)
    author = db.Column(db.String(10))
    pubdate = db.Column(db.DateTime, default=datetime.datetime.now)
