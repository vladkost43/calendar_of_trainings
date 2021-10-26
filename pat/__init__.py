import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_bcrypt import Bcrypt



app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba246'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://vlad:123456@localhost/pat_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt()
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "kostinvlad83@gmail.com"
app.config['MAIL_PASSWORD'] = "hesoyam123"
mail = Mail(app)
csrf.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from pat.group.group import Group
from pat.gender.gender import Gender
from pat.specialization.specialization import Specialization
from pat.user.user import User
from pat.trainer.trainer import Trainer
from pat.learner.learner import Learner
from pat.training.training import Training
from pat.trainer.routes import trainers
from pat.learner.routes import learners
from pat.training.routes import trainings
from pat.user.routes import user

app.register_blueprint(user)
app.register_blueprint(learners)
app.register_blueprint(trainers)
app.register_blueprint(trainings)
