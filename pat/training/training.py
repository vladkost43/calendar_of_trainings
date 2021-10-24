from datetime import datetime


from flask_login import UserMixin
from sqlalchemy import case, and_
from sqlalchemy.ext.hybrid import hybrid_property


from pat import db


class Training(UserMixin, db.Model):
    """
    User model
    """
    __tablename__ = 'training'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    description = db.Column(db.String(1000), unique=False)
    place = db.Column(db.String(128))
    status = db.Column(db.String(128))
    number = db.Column(db.Integer())
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship('User')

    training_start = db.Column(db.DateTime, default=datetime.utcnow)
    training_end = db.Column(db.DateTime, default=datetime.utcnow)

    learner = db.relationship('User',
                              secondary="training_user",
                              back_populates="training")
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.id'))
    specialization = db.relationship('Specialization')

    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'))
    gender = db.relationship('Gender')


    def __repr__(self):
        return "<User: {0}>".format(self.id)


    @hybrid_property
    def status(self):
        """
        Method for post status< after checking event_date
        """
        self.training_start = datetime.strptime(str(self.training_start), "%Y-%m-%d %H:%M:%S")
        if self.training_start > datetime.now() and len(self.learner) <self.number:
            return "open"
        if self.training_start <= datetime.now() or self.training_end <= datetime.now() or len(self.learner) >= self.number:
            return "closed"

    @status.expression
    def status(self):
        print(self.learner)
        return case([
            (self.training_start > datetime.now(), "open"),
        ], else_="closed")


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
