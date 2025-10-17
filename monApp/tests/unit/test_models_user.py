from monApp.models import User

def test_user_init(testapp):
    with testapp.app_context():
        user = User.query.get("CDAL")
        assert user.Login == "CDAL"

def test_user_get_id(testapp):
    with testapp.app_context():
        user = User.query.get("CDAL")
        assert user.get_id() == "CDAL"

def test_load_user(testapp):
    """Test de la fonction load_user"""
    with testapp.app_context():
        user = User.load_user("CDAL")
        assert user is not None
        assert user.Login == "CDAL"

def test_load_user_not_found(testapp):
    """Test de la fonction load_user avec un utilisateur inexistant"""
    with testapp.app_context():
        user = User.load_user("NONEXISTENT")
        assert user is None