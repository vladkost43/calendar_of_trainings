from datetime import datetime

from flask_login import UserMixin
from pat import db
from sqlalchemy_utils import PhoneNumberType
class TrainerSpecializationModel(db.Model):
    """
    Many-to-Many relationship model between Event and Authors
    """

    __tablename__ = 'trainer_specialization'

    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'), primary_key=True)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.id'), primary_key=True, nullable=False)


    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Trainer(UserMixin, db.Model):
    """
    User model
    """
    __tablename__ = 'trainer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    birthday_date = db.Column(db.DateTime, default=datetime.utcnow)
    phone_number = db.Column(PhoneNumberType())
    biography = db.Column(db.String(500), unique=True)
    register = db.Column(db.Boolean)
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'), nullable=False)
    user = db.relationship("User", uselist=False, backref="trainers")
    specialization = db.relationship('Specialization',
                              secondary="trainer_specialization",
                              back_populates="trainer")


    def __repr__(self):
        return "<{0} {1}>".format(self.user.first_name, self.user.last_name)
