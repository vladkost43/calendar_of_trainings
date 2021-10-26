import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import IntegerField, URLField, DateTimeField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange, url

from pat import Gender
from pat.trainer.forms import specialization_query


def gender_query():
    return Gender.query


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
