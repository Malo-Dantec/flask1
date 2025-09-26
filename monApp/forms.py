from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FloatField
from wtforms.validators import DataRequired, NumberRange
class FormAuteur(FlaskForm):
    idA=HiddenField('idA')
    Nom = StringField ('Nom', validators =[DataRequired()])
    
class FormLivre(FlaskForm):
    idL=HiddenField('idL')
    prix = FloatField('Prix', validators=[DataRequired(), NumberRange(min=0, message='Le prix doit être positif')])
    
from wtforms import PasswordField
from . models import User
from hashlib import sha256
class LoginForm(FlaskForm):
    Login = StringField ('Identifiant')
    Password = PasswordField ('Mot de passe')
    next = HiddenField()
    def get_authenticated_user(self):
        unUser = User.query.get(self.Login.data)
        if unUser is None:
            return None
        m = sha256()
        m.update(self.Password.data.encode())
        passwd = m.hexdigest()
        return unUser if passwd == unUser.Password else None
    
class RegisterForm(FlaskForm):
    Login = StringField ('Identifiant', validators =[DataRequired()])
    Password = PasswordField ('Mot de passe', validators =[DataRequired()])
    next = HiddenField()
    def get_registered_user(self):
        unUser = User.query.get(self.Login.data)
        if unUser is not None:
            return None
        m = sha256()
        m.update(self.Password.data.encode())
        passwd = m.hexdigest()
        newUser = User(Login=self.Login.data, Password=passwd)
        return newUser