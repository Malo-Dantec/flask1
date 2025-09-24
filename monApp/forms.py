from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FloatField
from wtforms.validators import DataRequired, NumberRange
class FormAuteur(FlaskForm):
    idA=HiddenField('idA')
    Nom = StringField ('Nom', validators =[DataRequired()])
    
class FormLivre(FlaskForm):
    idL=HiddenField('idL')
    prix = FloatField('Prix', validators=[DataRequired(), NumberRange(min=0, message='Le prix doit être positif')])