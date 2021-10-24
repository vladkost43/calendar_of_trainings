from pat import db

class Specialization(db.Model):
    """
    Group model
    Many-to-one relationship model between User and Group
    """
    __tablename__ = 'specialization'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specialization = db.Column(db.String(50), unique=True)
    color = db.Column(db.String(50), unique=True)
    trainer = db.relationship('Trainer',
                             secondary="trainer_specialization",
                             back_populates="specialization")
    training = db.relationship('Training', back_populates='specialization', lazy="dynamic")


    def __init__(self, *args, **kwargs):
        super(Specialization, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "{0}".format(self.specialization)
