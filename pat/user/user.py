from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from pat import db, login_manager, app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    """
    User model
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    _password = db.Column(db.String(200))
    photo = db.Column(db.String(20), default='default.jpg')
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    creator = db.relationship('Training', back_populates='creator', cascade='all, delete')

    learner = db.Column(db.Integer, db.ForeignKey('learner.id'))
    trainer = db.Column(db.Integer, db.ForeignKey('trainer.id'))
    training = db.relationship('Training',
                              secondary="training_user",
                               back_populates="learner",
                              cascade='all, delete')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return "<User: {0} {1}>".format(self.first_name, self.last_name)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        """
        Method for hask password
        """
        if password is None:
            self._password = None
        else:
            self._password = generate_password_hash(password)

    def check_password(self, password):
        """
        Method for check password
        """
        if not self._password or not password:
            return False
        return check_password_hash(self._password, password)

