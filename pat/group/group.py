from pat import db

class Group(db.Model):
    """
    Group model
    Many-to-one relationship model between User and Group
    """
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='group')

    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<Group: {0}>".format(self.group)
