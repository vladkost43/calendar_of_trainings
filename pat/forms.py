import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FormField, FileField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.fields.html5 import DateField, IntegerField, URLField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, url
import phonenumbers
from pat import Group, Specialization, Gender
from pat.user.user import User



def group_query():
    return Group.query

def specialization_query():
    return Specialization.query

def specialization_query_trainer(user_id):
    return Specialization.query.get(current_user.id)

def gender_query():
    return Gender.query


class RegisterTreanerForm(FlaskForm):
    birthday_date = DateField('Birthday_date', validators=[DataRequired()], format='%Y-%m-%d')
    phone_number = StringField('Phone', validators=[DataRequired()])
    biography = StringField('Biography', validators=[DataRequired()])
    gender = QuerySelectField('Gender', query_factory=gender_query, allow_blank=False, get_label='gender')
    specialization = QuerySelectMultipleField('Specialization', query_factory=specialization_query, get_label='specialization')

    def validate_phone_number(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

    def validate_birthday_date(self, birthday_data):
        now = datetime.date.today()
        days = (365 * 18) + (18 / 4)
        back18 = now - datetime.timedelta(days=days)
        if birthday_data.data >= back18:
            raise ValidationError('Invalid birthday date(Age must be > 18)')



class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first_name = StringField('First_name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last_name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    picture = FileField('Download Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    trainer = FormField(RegisterTreanerForm)

    submit = SubmitField('Sign Up')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_first_name(self, first_name):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in self.first_name.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")

    def validate_last_name(self, last_name):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in self.last_name.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")


class RegisterLearnerForm(FlaskForm):
    birthday_date = DateField('Birthday_date', validators=[DataRequired()])
    weight = IntegerField('Weight', validators=[NumberRange(min=0, max=250)])
    height = IntegerField('Height', validators=[NumberRange(min=0, max=250)])
    gender = QuerySelectField('Gender', query_factory=gender_query, allow_blank=False, get_label='gender')
    phone_number = StringField('Phone', validators=[DataRequired()])


    def validate_phone_number(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

    def validate_birthday_date(self, birthday_data):
        now = datetime.date.today()
        days = (365 * 18) + (18 / 4)
        back18 = now - datetime.timedelta(days=days)
        if birthday_data.data >= back18:
            raise ValidationError('Invalid birthday date(Age must be > 18)')


class RegistrationLForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first_name = StringField('First_name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last_name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    learner = FormField(RegisterLearnerForm)
    submit = SubmitField('Sign Up')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_first_name(self, first_name):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in self.first_name.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")

    def validate_last_name(self, last_name):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in self.last_name.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationAdminForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first_name = StringField('First_name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last_name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_first_name(self, first_name):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in self.first_name.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")

    def validate_last_name(self, last_name):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in self.last_name.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")


class FilterTrainers(FlaskForm):
    specialization = QuerySelectField('Specialization', query_factory=specialization_query, get_label='specialization')
    submit = SubmitField('filter')


class FilterTrainings(FlaskForm):
    specialization = QuerySelectField('Specialization', query_factory=specialization_query, get_label='specialization')
    status= SelectField("Status")
    submit = SubmitField('filter')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first_name = StringField('First_name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last_name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class AccLearnerForm(FlaskForm):
    weight = IntegerField('Weight', validators=[NumberRange(min=0, max=250)])
    height = IntegerField('Height', validators=[NumberRange(min=0, max=250)])
    phone_number = StringField('Phone', validators=[DataRequired()])


    def validate_phone_number(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')



class UpdateLearnerAccountForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first_name = StringField('First_name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last_name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    learner = FormField(AccLearnerForm)

    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class AccTreanerForm(FlaskForm):
    phone_number = StringField('Phone', validators=[DataRequired()])
    biography = StringField('Biography', validators=[DataRequired()])

    def validate_phone_number(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class UpdateTrainerAccountForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first_name = StringField('First_name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last_name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    trainer = FormField(AccTreanerForm)

    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class UpdateAccountAdminForm(FlaskForm):
    first_name = StringField('First_name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last_name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')







class UpdateLearnerAccountAdminForm(FlaskForm):

    first_name = StringField('First_name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last_name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    learner = FormField(AccLearnerForm)

    submit = SubmitField('Update')




class UpdateTrainerAccountAdminForm(FlaskForm):
    first_name = StringField('First_name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last_name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    trainer = FormField(AccTreanerForm)

    submit = SubmitField('Update')


class CreateTrainingForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired(), Length(min=5, max=1000)])
    place = URLField(validators=[url()])
    training_start = DateTimeField('Training start', validators=[DataRequired()])
    training_end = DateTimeField('Training end', validators=[DataRequired()])
    specialization = QuerySelectField('Specialization', query_factory=specialization_query,
                                              allow_blank=False, get_label='specialization')
    gender = QuerySelectField('Gender', query_factory=gender_query, allow_blank=False, get_label='gender')
    number = IntegerField('Nubmer of people', validators=[NumberRange(min=0, max=30)])
    submit = SubmitField('Create training')

    def validate_training_end(self, training_end):
        if self.training_end.data <= self.training_start.data:
            raise ValidationError('Training and must be > training start')
        else:
            return True

    def validate_training_start(self, training_start):
        a = datetime.datetime.strptime(str(self.training_start.data), "%Y-%m-%d %H:%M:%S")
        if a < datetime.datetime.now():
            raise ValidationError('You can bot create past event')
        else:
            return True




class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
