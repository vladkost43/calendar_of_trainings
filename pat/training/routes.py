import datetime

from flask import render_template, flash, url_for, request, Blueprint
from werkzeug.utils import redirect
from pat import db, Training

from flask_login import current_user, login_required
from pat.training.forms import CreateTrainingForm
trainings = Blueprint('trainings', __name__)


@trainings.route("/training/<int:training_id>/delete", methods=['POST'])
@login_required
def delete_training(training_id):
    user = Training.query.get_or_404(training_id)
    db.session.delete(user)
    db.session.commit()
    flash('Training has been deleted!', 'success')
    return redirect(url_for('user.home'))


@trainings.route("/training/<int:training_id>/register", methods=['POST'])
@login_required
def register(training_id):
    training = Training.query.get_or_404(training_id)
    training.learner.append(current_user)
    db.session.commit()
    flash('You are registrated!', 'success')
    return redirect(url_for('user.home'))


@trainings.route("/training/<int:training_id>/unregister", methods=['POST'])
@login_required
def unregister(training_id):
    training = Training.query.get_or_404(training_id)
    training.learner.remove(current_user)
    db.session.commit()
    flash('You are unregistrated on training!', 'success')
    return redirect(url_for('user.home'))


@trainings.route('/create_training', methods=['GET', 'POST'])
@login_required
def create_training():
    form = CreateTrainingForm()
    if form.validate_on_submit():
        if form.specialization.data not in current_user.trainers.specialization:
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
        return redirect(url_for('user.home'))
    print(form.errors)
    return render_template('create_training.html', form=form)


@trainings.route("/training/<int:training_id>")
def training(training_id):
    trainings = Training.query.get_or_404(training_id)
    times = datetime.datetime.now()
    return render_template('training.html', trainings=trainings, time=times)


@trainings.route("/training/<int:training_id>/update", methods=['GET', 'POST'])
@login_required
def update_training(training_id):
    training = Training.query.get_or_404(training_id)
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
        return redirect(url_for('user.home'))
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
