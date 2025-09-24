import click, logging as lg
from .app import app, db

@app.cli.command()
@click.argument('filename')

def loaddb(filename):
    '''Creates the tables and populates them with data.'''
    # création de toutes les tables
    db.drop_all()
    db.create_all()
    # chargement de notre jeu de données
    import yaml
    with open(filename, 'r') as file:
        lesLivres = yaml.safe_load(file)
    # import des modèles
    from . models import Auteur,Livre
    # première passe : création de tous les auteurs
    lesAuteurs = {}
    for livre in lesLivres :
        auteur = livre["author"]
        if auteur not in lesAuteurs :
            objet = Auteur(Nom=auteur)
            db.session.add(objet)
            lesAuteurs[auteur] = objet
    db.session.commit ()
    # deuxième passe : création de tous les livres
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
    '''Creates all missing tables . '''
    db.create_all()
    lg.warning('Database synchronized!')

@app.cli.command()
@click.argument('login')
@click.argument('pwd')
def newuser (login, pwd):
    '''Adds a new user'''
    from . models import User
    from hashlib import sha256
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
    '''Changes the password of an existing user'''
    from . models import User
    from hashlib import sha256
    unUser = User.query.get(login)
    if unUser is None :
        lg.error('User ' + login + ' does not exist!')
        return
    m = sha256()
    m.update(pwd.encode())
    unUser.Password = m.hexdigest()
    db.session.commit()
    lg.warning('Password of user ' + login + ' changed!')