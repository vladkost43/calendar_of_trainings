from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from pat import Specialization
from pat.user.user import User


def specialization_query():
    return Specialization.query


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


class FilterTrainings(FlaskForm):
    specialization = QuerySelectField('Specialization', query_factory=specialization_query, get_label='specialization')
    status = SelectField("Status")
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


class UpdateAccountAdminForm(FlaskForm):
    first_name = StringField('First_name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last_name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')


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
