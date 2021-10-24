from pat import db

class Gender(db.Model):
    """
    Group model
    Many-to-one relationship model between User and Group
    """
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.String(50), unique=True)
    learner = db.relationship('Learner', backref='gender')
    trainer = db.relationship('Trainer', backref='gender')
    training = db.relationship('Training', back_populates='gender', lazy="dynamic")

    def __init__(self, *args, **kwargs):
        super(Gender, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<Gender: {0}>".format(self.gender)
