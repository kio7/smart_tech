from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, SelectField, RadioField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class waveletImageForm(FlaskForm):
    image = FileField('Upload Picture', validators=[FileAllowed(['jpg'], 'Only JPEG images allowed!')])
    submit = SubmitField('Submit')

class DCTImageForm(FlaskForm):
    image = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Only JPEG and PNG images allowed!'), DataRequired("Please select a file")])
    select = SelectField('Low pass aggressiveness', choices=[(0, "Passive"), (1, "Agressive"), (2, "Very aggressive")], default=0, coerce=int)
    submit = SubmitField('Submit')

class FFTImageForm(FlaskForm):
    image = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Only JPEG and PNG images allowed!'), DataRequired("Please select a file")])
    submit = SubmitField('Submit')

class RegionOfInterestForm(FlaskForm):
    morphological = SelectField('Select morphological operation', 
                                choices=[
                                    (0, 'None'), (1, 'Erosion'), 
                                    (2, 'Dilation'), (3, 'Closing'), 
                                    (4, 'Opening')],
                                default=0, coerce=int)
    sift = SelectField('Use SIFT features?', choices=[(0, 'No'), (1, 'Yes')], default=0, coerce=int)
    submit = SubmitField('Submit')
