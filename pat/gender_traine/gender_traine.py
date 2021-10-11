from pat import db


class GenderTraine(db.Model):
    """
    Group model
    Many-to-one relationship model between User and Group
    """
    __tablename__ = 'gender_traine'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender_traine = db.Column(db.String(50), unique=True)
    training = db.relationship('Training', back_populates='gender', lazy="dynamic")

    def __init__(self, *args, **kwargs):
        super(GenderTraine, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<Group: {0}>".format(self.gender_traine)
