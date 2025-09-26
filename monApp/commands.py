import click, logging as lg
from .app import app, db
from . models import User, Auteur, Livre
from hashlib import sha256

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    """Charge les données initiales dans la base de données"""
    db.drop_all()
    db.create_all()
    import yaml
    with open(filename, 'r') as file:
        lesLivres = yaml.safe_load(file)
    lesAuteurs = {}
    for livre in lesLivres :
        auteur = livre["author"]
        if auteur not in lesAuteurs :
            objet = Auteur(Nom=auteur)
            db.session.add(objet)
            lesAuteurs[auteur] = objet
    db.session.commit ()
    for livre in lesLivres :
        auteur = lesAuteurs[livre["author"]]
        objet = Livre(prix=livre["price"],
                    titre=livre["title"],
                    url=livre["url"],
                    img=livre["img"],
                    auteur = auteur
        )
        db.session.add(objet)
    db.session.commit()
    lg.warning('Database initialized!')

@app.cli.command()
def syncdb():
    """Synchronise la base de données avec les modèles"""
    db.create_all()
    lg.warning('Database synchronized!')

@app.cli.command()
@click.argument('login')
@click.argument('pwd')
def newuser (login, pwd):
    """Crée un nouvel utilisateur"""
    m = sha256()
    m.update(pwd.encode())
    unUser = User(Login=login ,Password =m.hexdigest())
    db.session.add(unUser)
    db.session.commit()
    lg.warning('User ' + login + ' created!')

@app.cli.command()
@click.argument('login')
@click.argument('pwd')
def newpasswrd (login, pwd):
    """Change le mot de passe d'un utilisateur existant"""
    unUser = User.query.get(login)
    if unUser is None :
        lg.error('User ' + login + ' does not exist!')
        return
    m = sha256()
    m.update(pwd.encode())
    unUser.Password = m.hexdigest()
    db.session.commit()
    lg.warning('Password of user ' + login + ' changed!')
