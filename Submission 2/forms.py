from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class waveletImageForm(FlaskForm):
    image = FileField('Upload Picture', validators=[FileAllowed(['jpg'], 'Only JPEG images allowed!')])
    submit = SubmitField('Submit')

class DCTImageForm(FlaskForm):
    image = FileField('Upload Picture', validators=[FileAllowed(['jpg'], 'Only JPEG images allowed!'), DataRequired("Please select a file")])
    select = SelectField('Low pass aggressiveness', choices=[(0, "Passive"), (1, "Agressive"), (2, "Very aggressive")], default=0, coerce=int)
    submit = SubmitField('Submit')