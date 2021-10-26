from flask import render_template, flash, url_for, request, Blueprint
from werkzeug.utils import redirect
from pat import app, Group, User,db, Learner
from flask_login import  login_required
from pat.learner.forms import RegistrationLForm

learners = Blueprint('learners', __name__)

@learners.route('/learner', methods=['GET', 'POST'])
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
        return redirect(url_for('user.home'))
    print(form.errors)
    return render_template('learner.html', form=form)

@learners.route("/learner_list")
def learner_list():
    page = request.args.get('page', 1, type=int)
    learner = Learner.query.order_by(Learner.birthday_date.desc()).paginate(page=page, per_page=5)
    return render_template('learner_list.html', learner=learner)

@learners.route("/learner/<int:learner_id>")
@login_required
def learner_one(learner_id):
    learner = Learner.query.get_or_404(learner_id)
    return render_template('learner_one.html', learner=learner)

@learners.route("/learner/<int:learner_id>/delete", methods=['POST'])
@login_required
def delete_learner(learner_id):
    learnert = Learner.query.get_or_404(learner_id)
    user = User.query.filter_by(learners=learnert).first()
    db.session.delete(learnert)
    db.session.delete(user)
    db.session.commit()
    flash('Learner has been deleted!', 'success')
    return redirect(url_for('user.home'))
