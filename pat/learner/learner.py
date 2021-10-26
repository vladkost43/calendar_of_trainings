from datetime import datetime

from flask_login import UserMixin
from pat import db
from sqlalchemy_utils import PhoneNumberType

class Learner(UserMixin, db.Model):
    """
    Learner model
    """
    __tablename__ = 'learner'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    birthday_date = db.Column(db.DateTime, default=datetime.utcnow)
    phone_number = db.Column(PhoneNumberType())
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'))
    user = db.relationship("User", uselist=False, backref="learners")

    def __repr__(self):
        return "{0}".format(self.user.email)
