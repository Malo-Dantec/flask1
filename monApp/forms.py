from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, HiddenField, FloatField, PasswordField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from hashlib import sha256
from .models import User

class FormAuteur(FlaskForm):
    """Formulaire pour les auteurs"""
    idA = HiddenField('idA')
    Nom = StringField('Nom', validators=[DataRequired()])

class FormLivre(FlaskForm):
    """Formulaire pour les livres"""
    idL = HiddenField("idL")
    titre = StringField("Titre", validators=[DataRequired()])
    prix = DecimalField("Prix", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Enregistrer")

class LoginForm(FlaskForm):
    """Formulaire de login"""
    Login = StringField('Identifiant')
    Password = PasswordField('Mot de passe')
    next = HiddenField()

    def get_authenticated_user(self):
        """Retourne l'utilisateur si les identifiants sont corrects, None sinon"""
        unUser = User.query.get(self.Login.data)
        if unUser is None:
            return None
        m = sha256()
        m.update(self.Password.data.encode())
        passwd = m.hexdigest()
        return unUser if passwd == unUser.Password else None

class RegisterForm(FlaskForm):
    """Formulaire d'inscription"""
    Login = StringField('Identifiant', validators=[DataRequired()])
    Password = PasswordField('Mot de passe', validators=[DataRequired()])
    next = HiddenField()

    def get_registered_user(self):
        """Retourne un nouvel utilisateur si l'identifiant n'existe pas, None sinon"""
        unUser = User.query.get(self.Login.data)
        if unUser is not None:
            return None
        m = sha256()
        m.update(self.Password.data.encode())
        passwd = m.hexdigest()
        newUser = User(Login=self.Login.data, Password=passwd)
        return newUser
