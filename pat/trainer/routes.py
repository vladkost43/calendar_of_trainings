
from flask import render_template, flash, url_for, request, Blueprint
from werkzeug.utils import redirect
from pat import Group, User, Trainer, db, Training

from flask_login import login_required
from pat.trainer.forms import RegistrationForm, FilterTrainers
from pat.user.routes import save_picture

trainers = Blueprint('trainers', __name__)


@trainers.route('/register_trainer', methods=['GET', 'POST'])
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
        return redirect(url_for('user.home'))
    print(form.errors)
    return render_template('index.html', form=form)


@trainers.route("/trainer_false", methods=['GET', 'POST'])
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


@trainers.route("/trainer_list", methods=['GET', 'POST'])
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


@trainers.route("/trainer/<int:trainer_id>")
@login_required
def trainer(trainer_id):
    trainers = Trainer.query.get_or_404(trainer_id)
    training = Training.query.filter_by(creator=trainers.user)
    return render_template('trainer.html', trainers=trainers, training=training)


@trainers.route("/trainer/<int:trainer_id>/delete", methods=['POST'])
@login_required
def delete_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    user = User.query.filter_by(trainers=trainer).first()
    db.session.delete(trainer)
    db.session.delete(user)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('user.home'))


@trainers.route("/trainer/<int:trainer_id>/update", methods=['GET', 'POST'])
@login_required
def update_trainer(trainer_id):
    train = Trainer.query.filter_by(id=trainer_id).update(dict(register=True))
    db.session.commit()
    flash('Trainer confirmed', 'success')
    return redirect(url_for('user.home'))
