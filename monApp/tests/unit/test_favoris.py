from monApp.models import User, Livre
def login(client, username, password, next_path):
    return client.post(
        "/login/",
        data={"Login": username, "Password": password, "next": next_path},
        follow_redirects=True
    )

def test_favoris_toggle_add(client, testapp):
    login(client, "CDAL", "AIGRE", "/favoris/")
    
    response = client.post('/favoris/toggle/1', follow_redirects=True)
    assert response.status_code == 200
    
    with testapp.app_context():
        user = User.query.filter_by(Login="CDAL").first()
        livre = Livre.query.get(1)
        assert user.est_favori(livre) is True

def test_favoris_toggle_remove(client, testapp):
    login(client, "CDAL", "AIGRE", "/favoris/")
    
    # test si le livre est déjà dans les favoris, si non ajouter
    with testapp.app_context():
        user = User.query.filter_by(Login="CDAL").first()
        livre = Livre.query.get(1)
        if not user.est_favori(livre):
            user.favoris.append(livre)
            testapp.db.session.commit()
    
    response = client.post('/favoris/toggle/1', follow_redirects=True)
    assert response.status_code == 200
    
    with testapp.app_context():
        user = User.query.filter_by(Login="CDAL").first()
        livre = Livre.query.get(1)
        assert user.est_favori(livre) is False

def test_favoris_page(client, testapp):
    login(client, "CDAL", "AIGRE", "/favoris/")
    
    response = client.get('/favoris/')
    assert response.status_code == 200
    
    with testapp.app_context():
        user = User.query.filter_by(Login="CDAL").first()
        for livre in user.favoris:
            assert livre.titre.encode() in response.data

def test_est_favoris(client, testapp):
    login(client, "CDAL", "AIGRE", "/favoris/")
    
    with testapp.app_context():
        user = User.query.filter_by(Login="CDAL").first()
        livre = Livre.query.get(1)
        
        if user.est_favori(livre):
            user.favoris.remove(livre)
            testapp.db.session.commit()
        
        assert user.est_favori(livre) is False
        
        user.favoris.append(livre)
        testapp.db.session.commit()
        
        assert user.est_favori(livre) is True
            
        
    