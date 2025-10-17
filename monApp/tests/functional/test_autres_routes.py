from monApp.tests.functional.test_routes_auteur import login

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Bienvenue' in response.data

def test_index_with_name(client):
    response = client.get('/index/?name=Alice')
    assert response.status_code == 200
    assert b'Bienvenue Alice' in response.data

def test_about(client):
    response = client.get('/about/')
    assert response.status_code == 200
    assert b'A propos' in response.data

def test_contact(client):
    response = client.get('/contact/')
    assert response.status_code == 200
    assert b'Contact' in response.data

def test_logout(client):
    login(client, "CDAL", "AIGRE", "/")
    response = client.get('/logout/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Se connecter' in response.data

def test_login_page(client):
    response = client.get('/login/')
    assert response.status_code == 200
    assert b'Connexion' in response.data

def test_login_success(client):
    response = login(client, "CDAL", "AIGRE", "/")
    assert response.status_code == 200
    assert b'Bienvenue' in response.data

def test_register_page(client):
    response = client.get('/register/')
    assert response.status_code == 200
    assert b'Inscription' in response.data

def test_register_success(client, testapp):
    response = client.post(
        "/register/",
        data={"Login": "NewUser", "Password": "newpass", "next": ""},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Connexion' in response.data
    
    with testapp.app_context():
        from monApp.models import User
        user = User.query.get("NewUser")
        assert user is not None

def test_register_existing_user(client):
    response = client.post(
        "/register/",
        data={"Login": "CDAL", "Password": "test", "next": ""},
        follow_redirects=True
    )
    assert response.status_code == 200