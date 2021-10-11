from datetime import datetime

from flask_login import UserMixin
from pat import db


class Training(UserMixin, db.Model):
    """
    User model
    """
    __tablename__ = 'training'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    description = db.Column(db.String(1000), unique=True)
    place = db.Column(db.String(128))
    lst_name = db.Column(db.String(128))
    status = db.Column(db.String(128))
    trainer = db.Column(db.String(128))

    training_start = db.Column(db.DateTime, default=datetime.utcnow)
    training_end = db.Column(db.DateTime, default=datetime.utcnow)

    learner = db.relationship('User',
                              secondary="training_user",
                              back_populates="training")
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.id'))
    specialization = db.relationship('Specialization')



    register = db.Column(db.Boolean)

    gender_id = db.Column(db.Integer, db.ForeignKey('gender_traine.id'))
    gender = db.relationship('GenderTraine')


    def __repr__(self):
        return "<User: {0}>".format(self.id)


class TrainingUserModel(db.Model):
    """
    Many-to-Many relationship model between Event and Authors
    """

    __tablename__ = 'training_user'

    training_id = db.Column(db.Integer, db.ForeignKey('training.id', ondelete="CASCADE"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)


    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
