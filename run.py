import os
import secrets

from PIL import Image
from flask import render_template, flash, url_for, request, current_app

from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

from pat import app, Group, User, Trainer, db, Learner
from pat.forms import RegistrationForm, RegistrationLForm, LoginForm, RegistrationAdminForm, FilterTrainers, \
    UpdateAccountForm, UpdateTrainerAccountForm, UpdateLearnerAccountForm
from flask_login import login_user, current_user, logout_user, login_required


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
@app.route("/home")
def home():
    trainer = Trainer.query.filter_by(register=False)
    return render_template('home.html', trainer=trainer)


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
    elif current_user.group_id == 2:
        form = UpdateTrainerAccountForm()
    else:
        form = UpdateLearnerAccountForm()
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
                           image_file=image_file, form=form)


if __name__ == '__main__':
    app.run(debug=True)
