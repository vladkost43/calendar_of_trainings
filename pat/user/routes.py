import os
import secrets
from PIL import Image
from flask import render_template, flash, url_for, request, current_app, Blueprint
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect
from pat import Group, User, db, Training, mail

from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from pat.learner.forms import UpdateLearnerAccountForm
from pat.trainer.forms import UpdateTrainerAccountForm
from pat.user.forms import RegistrationAdminForm, LoginForm,\
    FilterTrainings, UpdateAccountForm, UpdateAccountAdminForm, \
    RequestResetForm, ResetPasswordForm

user = Blueprint('user', __name__)


@user.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    form = RegistrationAdminForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data,
                    group=Group.query.get(3))
        db.session.add(user)
        db.session.commit()
        flash('Admin account has been created! You are now able to log in', 'success')
        print(form.errors)
        return redirect(url_for('user.home'))
    print(form.errors)
    return render_template('admin_registrate.html', form=form)


@user.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if user.trainers and user.trainers.register is False:
                flash('Admin must check your account', 'danger')
            else:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('user.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'info')
    return render_template('login.html', title='Login', form=form)


@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('user.home'))


@user.route("/")
@user.route("/home", methods=['GET', 'POST'])
def home():
    form = FilterTrainings()
    status = ["open", "closed"]
    form.status.choices = status
    if form.validate_on_submit():
        training = Training.query\
                .filter_by(specialization=form.specialization.data, status=form.status.data)
    else:
        training = Training.query.all()
    return render_template('home.html', training=training, form=form)


@user.route("/admin_list")
def admin_list():
    page = request.args.get('page', 1, type=int)
    admin = User.query.filter_by(group_id=3).paginate(page=page, per_page=5)
    return render_template('admin_list.html', admin=admin)


@user.route("/admin/<int:admin_id>")
@login_required
def admin(admin_id):
    admins = User.query.get_or_404(admin_id)
    return render_template('admin.html', admins=admins)


@user.route("/admin/<int:admin_id>/delete", methods=['POST'])
@login_required
def delete_admin(admin_id):
    user = User.query.get_or_404(admin_id)
    db.session.delete(user)
    db.session.commit()
    flash('Admin has been deleted!', 'success')
    return redirect(url_for('user.home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@user.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if current_user.group_id == 3 or current_user.group_id == 4:
         form = UpdateAccountForm()
         training = []
    elif current_user.group_id == 2:
        form = UpdateTrainerAccountForm()
        training = Training.query \
            .filter_by(creator=current_user)
    else:
        form = UpdateLearnerAccountForm()
        training = Training.query \
            .filter(Training.learner.contains(current_user))
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.photo = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        if current_user.group_id == 2:
            current_user.trainers.phone_number = form.trainer.phone_number.data
            current_user.trainers.boigraphy = form.trainer.biography.data
            current_user.trainers.specialization = form.trainer.specialization.data
        if current_user.group_id == 1:
            current_user.learners.phone_number = form.learner.phone_number.data
            current_user.learners.weight = form.learner.weight.data
            current_user.learners.height = form.learner.height.data
            current_user.learners.gender = form.learner.gender.data

        db.session.commit()
        flash('Your account has been updated!', 'success')
        print(form.errors)
        return redirect(url_for('user.account'))
    elif request.method == 'GET':

        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        if current_user.group_id == 2:
            form.trainer.phone_number.data = "+38 {0}".format(current_user.trainers.phone_number)
            form.trainer.biography.data = current_user.trainers.biography
            form.trainer.specialization.data = current_user.trainers.specialization

        if current_user.group_id == 1:
            form.learner.phone_number.data = "+38 {0}".format(current_user.learners.phone_number)
            form.learner.weight.data = current_user.learners.weight
            form.learner.height.data = current_user.learners.height
            form.learner.gender.data = current_user.learners.gender
    image_file = url_for('static', filename='profile_pics/' + current_user.photo)
    print(form.errors)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, training=training)


@user.route("/user/<int:user_id>/update", methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.group_id == 3 or user.group_id == 4:
        form = UpdateAccountAdminForm()
    elif user.group_id == 2:
        form = UpdateTrainerAccountForm()
    else:
        form = UpdateLearnerAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.photo = picture_file
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        if user.group_id == 2:
            user.trainers.phone_number = form.trainer.phone_number.data
            user.trainers.boigraphy = form.trainer.biography.data
        if user.group_id == 1:
            user.learners.phone_number = form.learner.phone_number.data
            user.learners.weight = form.learner.weight.data
            user.learners.height = form.learner.height.data

        db.session.commit()
        flash('User account has been updated!', 'success')
        print(form.errors)
        return redirect(url_for('user.home'))
    elif request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name

        if user.group_id == 2:
            form.trainer.phone_number.data = "+38 {0}".format(user.trainers.phone_number)
            form.trainer.biography.data = user.trainers.biography
        if user.group_id == 1:
            form.learner.phone_number.data = "+38 {0}".format(user.learners.phone_number)
            form.learner.weight.data = user.learners.weight
            form.learner.height.data = user.learners.height
    image_file = url_for('static', filename='profile_pics/' + user.photo)
    print(form.errors)
    return render_template('user_update.html', title='Account', user=user,
                           image_file=image_file, form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@user.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('user.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@user.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('user.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('user.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
