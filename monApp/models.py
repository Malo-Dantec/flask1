from .app import db, login_manager
from flask_login import UserMixin

class Auteur(db.Model):
    """Modèle pour les auteurs"""
    idA = db.Column( db.Integer, primary_key=True )
    Nom = db.Column( db.String(100) )
    
    def __init__(self, Nom):
        self.Nom = Nom

    def __repr__ (self ):
        return "<Auteur (%d) %s>" % (self.idA , self.Nom)

class Livre(db.Model):
    """Modèle pour les livres"""
    idL = db.Column( db.Integer, primary_key=True )
    prix = db.Column( db.Float )
    titre = db.Column( db.String(255) )
    url = db.Column( db.String(255) )
    img = db.Column( db.String(255) )

    auteur_id = db.Column (db.Integer , db.ForeignKey ("auteur.idA") )
    auteur = db.relationship ("Auteur", backref =db.backref ("livres", lazy="dynamic") )

    def __init__(self, titre, auteur, prix=0.0, url="", img=""):
        self.titre = titre
        self.auteur = auteur
        self.prix = prix
        self.url = url
        self.img = img

    def __repr__ (self ):
        return "<Livre (%d) %s>" % (self.idL , self.titre)

favoris = db.Table('favoris',
    db.Column('user_login', db.String(50), db.ForeignKey('user.Login'), primary_key=True),
    db.Column('livre_id', db.Integer, db.ForeignKey('livre.idL'), primary_key=True)
)

class User(db.Model, UserMixin):
    """Modèle pour les utilisateurs"""
    Login = db.Column (db.String(50), primary_key=True)
    Password = db.Column (db.String(64))
    
    favoris = db.relationship('Livre', secondary=favoris, backref=db.backref('favori_par', lazy='dynamic'))

    def get_id(self):
        """Récupère l'identifiant de l'utilisateur"""
        return self.Login

    @login_manager.user_loader
    def load_user(username):
        """Charge un utilisateur par son identifiant"""
        return User.query.get(username)
    
    def est_favori(self, livre):
        """Vérifie si un livre est dans les favoris de l'utilisateur"""
        return livre in self.favoris