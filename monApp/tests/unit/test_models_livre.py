from monApp.models import Livre, Auteur
from monApp import db

def test_livre_init(testapp):
    with testapp.app_context():
        auteur = Auteur.query.get(1)
        livre = Livre("Le Seigneur des Anneaux", auteur, prix=25.99, url="http://example.com", img="lotr.jpg")
        assert livre.titre == "Le Seigneur des Anneaux"
        assert livre.prix == 25.99
        assert livre.auteur == auteur

def test_livre_repr(testapp):
    with testapp.app_context():
        livre = Livre.query.get(1)
        assert repr(livre) == "<Livre (1) Les Misérables>"

def test_livre_default_values(testapp):
    with testapp.app_context():
        auteur = Auteur.query.get(1)
        livre = Livre("Mon Livre", auteur)
        assert livre.prix == 0.0
        assert livre.url == ""
        assert livre.img == ""