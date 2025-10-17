def login(client, username, password, next_path):
    return client.post(
        "/login/",
        data={"Login": username, "Password": password, "next": next_path},
        follow_redirects=True
    )

def test_login_page_get(client):
    response = client.get('/login/')
    assert response.status_code == 200
    assert b'Connexion' in response.data

def test_login_success(client):
    response = login(client, "CDAL", "AIGRE", "/")
    assert response.status_code == 200
    assert b'Bienvenue' in response.data

def test_login_failure(client):
    response = client.post(
        "/login/",
        data={"Login": "CDAL", "Password": "wrongpass", "next": ""},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Connexion' in response.data

def test_login_nonexistent_user(client):
    response = client.post(
        "/login/",
        data={"Login": "NONEXISTENT", "Password": "pass", "next": ""},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Connexion' in response.data

def test_login_with_next(client):
    response = login(client, "CDAL", "AIGRE", "/auteurs/")
    assert response.status_code == 200

def test_logout(client):
    login(client, "CDAL", "AIGRE", "/")
    response = client.get('/logout/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Bienvenue' in response.data

def test_register_page_get(client):
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
    assert b'Inscription' in response.data

def test_register_empty_fields(client):
    response = client.post(
        "/register/",
        data={"Login": "", "Password": "", "next": ""},
        follow_redirects=True
    )
    assert response.status_code == 200