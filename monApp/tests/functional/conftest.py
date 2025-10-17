import pytest

def login(client, username, password, next_path):
    """Simule la connexion d'un utilisateur"""
    return client.post(
        "/login/",
        data={"Login": username, "Password": password, "next": next_path},
        follow_redirects=True
    )

@pytest.fixture
def login_user(client):
    """Fixture pour se connecter rapidement"""
    def _login():
        return login(client, "CDAL", "AIGRE", "/")
    return _login