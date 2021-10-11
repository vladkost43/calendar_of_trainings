from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FormField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
import phonenumbers
from pat import Group, Specialization, Gender
from pat.user.user import User

def group_query():
    return Group.query

def specialization_query():
    return Specialization.query

def gender_query():
    return Gender.query


class RegisterTreanerForm(FlaskForm):
    birthday_date = DateField('Birthday_date', validators=[DataRequired()])
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
