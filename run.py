import os
import secrets

from PIL import Image
from flask import render_template, flash, url_for, request, current_app
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

from pat import app, Group, User, Trainer, db, Learner, Training, mail
from pat.forms import RegistrationForm, RegistrationLForm, LoginForm, RegistrationAdminForm, FilterTrainers, \
    UpdateAccountForm, UpdateTrainerAccountForm, UpdateLearnerAccountForm, UpdateAccountAdminForm, \
    UpdateTrainerAccountAdminForm, UpdateLearnerAccountAdminForm, CreateTrainingForm, FilterTrainings, RequestResetForm, \
    ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route('/register_trainer', methods=['GET', 'POST'])
def register_trainer():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.picture.data)
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data,
                    group=Group.query.get(2))
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.photo = picture_file
        trainers1 = Trainer(birthday_date=form.trainer.birthday_date.data,
                            phone_number=form.trainer.phone_number.data,
                            biography=form.trainer.biography.data,
                            gender=form.trainer.gender.data,
                            register=False,
                            specialization=form.trainer.specialization.data
                            )
        user.trainers = trainers1
        db.session.add_all([user, trainers1])
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        print(form.errors)
        return redirect(url_for('home'))
    print(form.errors)
    return render_template('index.html', form=form)


@app.route('/register_admin', methods=['GET', 'POST'])
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
        return redirect(url_for('home'))
    print(form.errors)
    return render_template('admin_registrate.html', form=form)


@app.route('/learner', methods=['GET', 'POST'])
def learner():
    form = RegistrationLForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data,
                    group=Group.query.get(1))
        learners1 = Learner(birthday_date=form.learner.birthday_date.data,
                            height=form.learner.height.data,
                            weight=form.learner.weight.data,
                            gender=form.learner.gender.data,
                            phone_number=form.learner.phone_number.data
                            )
        user.learners = learners1

        db.session.add_all([user, learners1])
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        print(form.errors)
        return redirect(url_for('home'))
    print(form.errors)
    return render_template('learner.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if user.trainers and user.trainers.register == False:
                flash('Admin must check your account', 'danger')
            else:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'info')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/trainer_false", methods=['GET', 'POST'])
def trainer_false():
    form = FilterTrainers()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        trainer = Trainer.query \
            .filter_by(register=False and Trainer.specialization.contains(form.specialization.data)) \
            .paginate(page=page, per_page=5)
    else:
        trainer = Trainer.query \
            .filter_by(register=False) \
            .paginate(page=page, per_page=5)
    return render_template('trainerfalse.html', trainer=trainer, form=form)


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
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


@app.route("/trainer_list", methods=['GET', 'POST'])
def trainer_list_true():
    form = FilterTrainers()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        trainer = Trainer.query\
            .filter_by(register=True and Trainer.specialization.contains(form.specialization.data))\
            .paginate(page=page, per_page=5)
    else:
        trainer = Trainer.query\
            .filter_by(register=True)\
            .paginate(page=page, per_page=5)
    return render_template('trainer_list.html', trainer=trainer, form=form)


@app.route("/learner_list")
def learner_list():
    page = request.args.get('page', 1, type=int)
    learner = Learner.query.order_by(Learner.birthday_date.desc()).paginate(page=page, per_page=5)
    return render_template('learner_list.html', learner=learner)


@app.route("/admin_list")
def admin_list():
    page = request.args.get('page', 1, type=int)
    admin = User.query.filter_by(group_id=3).paginate(page=page, per_page=5)
    return render_template('admin_list.html', admin=admin)


@app.route("/trainer/<int:trainer_id>")
@login_required
def trainer(trainer_id):
    trainers = Trainer.query.get_or_404(trainer_id)
    return render_template('trainer.html', trainers=trainers)


@app.route("/admin/<int:admin_id>")
@login_required
def admin(admin_id):
    admins = User.query.get_or_404(admin_id)
    return render_template('admin.html', admins=admins)


@app.route("/learner/<int:learner_id>")
@login_required
def learner_one(learner_id):
    learner = Learner.query.get_or_404(learner_id)
    return render_template('learner_one.html', learner=learner)


@app.route("/trainer/<int:trainer_id>/delete", methods=['POST'])
@login_required
def delete_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    user = User.query.filter_by(trainers=trainer).first()
    db.session.delete(trainer)
    db.session.delete(user)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/learner/<int:learner_id>/delete", methods=['POST'])
@login_required
def delete_learner(learner_id):
    learnert = Learner.query.get_or_404(learner_id)
    user = User.query.filter_by(learners=learnert).first()
    db.session.delete(learnert)
    db.session.delete(user)
    db.session.commit()
    flash('Learner has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/admin/<int:admin_id>/delete", methods=['POST'])
@login_required
def delete_admin(admin_id):
    user = User.query.get_or_404(admin_id)
    db.session.delete(user)
    db.session.commit()
    flash('Admin has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/training/<int:training_id>/delete", methods=['POST'])
@login_required
def delete_training(training_id):
    user = Training.query.get_or_404(training_id)
    db.session.delete(user)
    db.session.commit()
    flash('Training has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/training/<int:training_id>/register", methods=['POST'])
@login_required
def register(training_id):
    training = Training.query.get_or_404(training_id)
    training.learner.append(current_user)
    db.session.commit()
    flash('You are registrated!', 'success')
    return redirect(url_for('home'))


@app.route("/training/<int:training_id>/unregister", methods=['POST'])
@login_required
def unregister(training_id):
    training = Training.query.get_or_404(training_id)
    training.learner.remove(current_user)
    db.session.commit()
    flash('You are unregistrated on training!', 'success')
    return redirect(url_for('home'))




@app.route("/post/<int:trainer_id>/update", methods=['GET', 'POST'])
@login_required
def update_trainer(trainer_id):
    train = Trainer.query.filter_by(id=trainer_id).update(dict(register=True))
    db.session.commit()
    flash('Trainer confirmed', 'success')
    return redirect(url_for('home'))


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


@app.route("/account", methods=['GET', 'POST'])
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
        if current_user.group_id == 1:
            current_user.learners.phone_number = form.learner.phone_number.data
            current_user.learners.weight = form.learner.weight.data
            current_user.learners.height = form.learner.height.data

        db.session.commit()
        flash('Your account has been updated!', 'success')
        print(form.errors)
        return redirect(url_for('account'))
    elif request.method == 'GET':

        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        if current_user.group_id == 2:
            form.trainer.phone_number.data = "+38 {0}".format(current_user.trainers.phone_number)
            form.trainer.biography.data = current_user.trainers.biography

        if current_user.group_id == 1:
            form.learner.phone_number.data = "+38 {0}".format(current_user.learners.phone_number)
            form.learner.weight.data = current_user.learners.weight
            form.learner.height.data = current_user.learners.height
    image_file = url_for('static', filename='profile_pics/' + current_user.photo)
    print(form.errors)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, training=training)


@app.route("/user/<int:user_id>/update", methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.group_id == 3 or user.group_id == 4:
        form = UpdateAccountAdminForm()
    elif user.group_id == 2:
        form = UpdateTrainerAccountAdminForm()
    else:
        form = UpdateLearnerAccountAdminForm()
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
        return redirect(url_for('home'))
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


@app.route('/create_training', methods=['GET', 'POST'])
@login_required
def create_training():
    form = CreateTrainingForm()
    if form.validate_on_submit():
        if not form.specialization.data in current_user.trainers.specialization:
            flash('Choose trainer specializations', 'danger')
            return redirect(url_for('create_training'))
        training = Training(description=form.description.data,
                    place=form.place.data,
                    creator = current_user,
                    training_start=form.training_start.data,
                    training_end=form.training_end.data,
                    specialization=form.specialization.data,
                    gender=form.gender.data,
                    number=form.number.data)
        db.session.add(training)
        db.session.commit()
        flash('Training has been created!', 'success')
        print(form.errors)
        return redirect(url_for('home'))
    print(form.errors)
    return render_template('create_training.html', form=form)

@app.route("/training/<int:training_id>")
def training(training_id):
    trainings = Training.query.get_or_404(training_id)
    return render_template('training.html', trainings=trainings)

@app.route("/training/<int:training_id>/update", methods=['GET', 'POST'])
@login_required
def update_training(training_id):
    training= Training.query.get_or_404(training_id)
    form = CreateTrainingForm()
    if form.validate_on_submit():

        training.training_start = form.training_start.data
        training.training_end = form.training_end.data
        training.description = form.description.data
        training.place = form.place.data
        training.gender = form.gender.data
        training.specialization = form.specialization.data
        training.number = form.number.data
        db.session.commit()
        flash('User account has been updated!', 'success')
        print(form.errors)
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.training_start.data = training.training_start
        form.training_end.data = training.training_end
        form.description.data = training.description
        form.place.data = training.place
        form.gender.data = training.gender
        form.specialization.data = training.specialization
        form.number.data = training.number

    print(form.errors)
    return render_template('training_update.html', title='Account', trtaining=training,
                            form=form)


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


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


if __name__ == '__main__':
    app.run(debug=True)
