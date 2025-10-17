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
    from monApp.app import login_manager
    with testapp.app_context():
        user = login_manager.user_loader("CDAL")
        assert user is not None
        assert user.Login == "CDAL"

def test_load_user_not_found(testapp):
    from monApp.app import login_manager
    with testapp.app_context():
        user = login_manager.user_loader("NONEXISTENT")
        assert user is None