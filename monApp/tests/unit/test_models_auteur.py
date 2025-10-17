from monApp.models import Auteur

def test_auteur_init():
    auteur = Auteur("Cricri DAL")
    assert auteur.Nom == "Cricri DAL"

def test_auteur_repr(testapp):
    with testapp.app_context():
        auteur = Auteur.query.get(1)
        assert repr(auteur) == "<Auteur (1) Victor Hugo>"