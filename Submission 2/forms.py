import os
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, BooleanField, IntegerField, FileField
from wtforms.validators import NumberRange
from flask_wtf.file import FileAllowed

class waveletImageForm(FlaskForm):
    image = FileField('Upload Picture', validators=[FileAllowed(['jpg'], 'Only JPEG images allowed!')])
    submit = SubmitField('Submit')