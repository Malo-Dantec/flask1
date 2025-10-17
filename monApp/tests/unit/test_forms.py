from monApp.forms import LoginForm, RegisterForm, FormAuteur, FormLivre
from monApp.models import User
from monApp import db
from hashlib import sha256

def test_login_form_get_authenticated_user_success(testapp):
    """Test authentification réussie"""
    with testapp.app_context():
        form = LoginForm()
        form.Login.data = "CDAL"
        form.Password.data = "AIGRE"
        
        user = form.get_authenticated_user()
        assert user is not None
        assert user.Login == "CDAL"

def test_login_form_get_authenticated_user_wrong_password(testapp):
    """Test authentification avec mauvais mot de passe"""
    with testapp.app_context():
        form = LoginForm()
        form.Login.data = "CDAL"
        form.Password.data = "wrongpassword"
        
        user = form.get_authenticated_user()
        assert user is None

def test_login_form_get_authenticated_user_nonexistent(testapp):
    """Test authentification avec utilisateur inexistant"""
    with testapp.app_context():
        form = LoginForm()
        form.Login.data = "NonExistent"
        form.Password.data = "password"
        
        user = form.get_authenticated_user()
        assert user is None

def test_register_form_get_registered_user_success(testapp):
    """Test inscription d'un nouvel utilisateur"""
    with testapp.app_context():
        form = RegisterForm()
        form.Login.data = "NewTestUser"
        form.Password.data = "testpassword"
        
        user = form.get_registered_user()
        assert user is not None
        assert user.Login == "NewTestUser"
        # Vérifier que le mot de passe est hashé
        assert len(user.Password) == 64

def test_register_form_get_registered_user_existing(testapp):
    """Test inscription avec un login déjà existant"""
    with testapp.app_context():
        form = RegisterForm()
        form.Login.data = "CDAL"  # Utilisateur déjà existant
        form.Password.data = "password"
        
        user = form.get_registered_user()
        assert user is None

def test_form_auteur_fields(testapp):
    """Test des champs du formulaire auteur"""
    with testapp.app_context():
        form = FormAuteur()
        assert hasattr(form, 'idA')
        assert hasattr(form, 'Nom')

def test_form_livre_fields(testapp):
    """Test des champs du formulaire livre"""
    with testapp.app_context():
        form = FormLivre()
        assert hasattr(form, 'idL')
        assert hasattr(form, 'titre')
        assert hasattr(form, 'prix')
        assert hasattr(form, 'submit')

def test_login_form_fields(testapp):
    """Test des champs du formulaire login"""
    with testapp.app_context():
        form = LoginForm()
        assert hasattr(form, 'Login')
        assert hasattr(form, 'Password')
        assert hasattr(form, 'next')

def test_register_form_fields(testapp):
    """Test des champs du formulaire register"""
    with testapp.app_context():
        form = RegisterForm()
        assert hasattr(form, 'Login')
        assert hasattr(form, 'Password')
        assert hasattr(form, 'next')