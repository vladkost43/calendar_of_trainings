from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba246'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://vlad:123456@localhost/pat_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(app)

db = SQLAlchemy(app)
csrf.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from pat.group.group import Group
from pat.gender.gender import Gender
from pat.gender_traine.gender_traine import GenderTraine
from pat.specialization.specialization import Specialization
from pat.user.user import User
from pat.trainer.trainer import Trainer
from pat.learner.learner import Learner
from pat.training.training import Training
