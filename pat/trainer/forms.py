import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FormField, FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import phonenumbers
from pat import Specialization, Gender
from pat.user.user import User


def specialization_query():
    return Specialization.query


def gender_query_user():
    return Gender.query.limit(2).all()


class RegisterTreanerForm(FlaskForm):
    birthday_date = DateField('Birthday_date', validators=[DataRequired()], format='%Y-%m-%d')
    phone_number = StringField('Phone', validators=[DataRequired()])
    biography = StringField('Biography', validators=[DataRequired()])
    gender = QuerySelectField('Gender', query_factory=gender_query_user, allow_blank=False, get_label='gender')
    specialization = QuerySelectMultipleField('Specialization',
                                              query_factory=specialization_query,
                                              get_label='specialization')

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


class FilterTrainers(FlaskForm):
    specialization = QuerySelectField('Specialization', query_factory=specialization_query, get_label='specialization')
    submit = SubmitField('filter')


class AccTreanerForm(FlaskForm):
    phone_number = StringField('Phone', validators=[DataRequired()])
    biography = StringField('Biography', validators=[DataRequired()])
    specialization = QuerySelectMultipleField('Specialization', query_factory=specialization_query,
                                              get_label='specialization')

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
