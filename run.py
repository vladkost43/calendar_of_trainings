from flask import render_template, flash, url_for, request

from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

from pat import app, Group, User, Trainer, db, Learner
from pat.forms import RegistrationForm, RegistrationLForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/register_trainer', methods=['GET', 'POST'])
def register_trainer():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data,
                    group=Group.query.get(2))
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
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route("/trainer_list_false")
def trainer_list():
    trainer = Trainer.query.filter_by(register=False)
    return render_template('trainer_list.html', trainer=trainer)

@app.route("/")
@app.route("/home")
def home():
    trainer = Trainer.query.filter_by(register=False)
    return render_template('home.html', trainer=trainer)



@app.route("/trainer_list")
def trainer_list_true():
    trainer = Trainer.query.filter_by(register=True)
    return render_template('trainer_list.html', trainer=trainer)


@app.route("/learner_list")
def learner_list():
    learner = Learner.query.all()
    return render_template('learner_list.html', learner=learner)


@app.route("/trainer/<int:trainer_id>")
@login_required
def trainer(trainer_id):
    trainers = Trainer.query.get_or_404(trainer_id)
    return render_template('trainer.html',  trainers=trainers)


@app.route("/learner/<int:learner_id>")
@login_required
def learner_one(learner_id):
    learner = Learner.query.get_or_404(learner_id)
    return render_template('learner_one.html',  learner=learner)


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


if __name__ == '__main__':
    app.run(debug=True)
