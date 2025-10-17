import os
from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, request, url_for, redirect, jsonify
from .app import app, db
from monApp.models import Auteur, Livre
from monApp.forms import FormAuteur, FormLivre, LoginForm, RegisterForm
from sqlalchemy import func

@app.route('/about/')
def about():
    """Page A propos"""
    return render_template("about.html", title="A propos")

@app.route('/contact/')
def contact():
    """Page Contact"""
    return render_template("contact.html", title="Contact")

@app.route('/')
@app.route('/index/')
def index():
    """Page d'accueil"""
    if len(request.args) == 0:
        return render_template("index.html", title="R3.01 Dev Web avec Flask", name="")
    else:
        param_name = request.args.get('name')
        return render_template("index.html", title="R3.01 Dev Web avec Flask", name=param_name)

@app.route('/auteurs/')
def getAuteurs():
    """Liste des auteurs, avec recherche et tri possibles"""
    query = request.args.get("q", "").strip()
    sort_by = request.args.get("sort", "nom")
    
    if query:
        lesAuteurs = Auteur.query.filter(Auteur.Nom.ilike(f"%{query}%"))
    else:
        lesAuteurs = Auteur.query
    
    if sort_by == "livres_asc":
        lesAuteurs = lesAuteurs.outerjoin(Livre).group_by(Auteur.idA).order_by(func.count(Livre.idL).asc())
    elif sort_by == "livres_desc":
        lesAuteurs = lesAuteurs.outerjoin(Livre).group_by(Auteur.idA).order_by(func.count(Livre.idL).desc())
    else:
        lesAuteurs = lesAuteurs.order_by(Auteur.Nom)
    
    lesAuteurs = lesAuteurs.all()
    return render_template("auteurs_list.html", title="Les Auteurs", auteurs=lesAuteurs, query=query, sort_by=sort_by)

@app.route('/auteurs/<idA>/update/')
@login_required
def updateAuteur(idA):
    """Formulaire de mise à jour d'un auteur"""
    unAuteur = Auteur.query.get(idA)
    unForm = FormAuteur(idA=unAuteur.idA, Nom=unAuteur.Nom)
    return render_template("auteur_update.html", selectedAuteur=unAuteur, updateForm=unForm)

@app.route('/auteur/save/', methods=("POST",))
@login_required
def saveAuteur():
    """Sauvegarde les modifications d'un auteur"""
    updatedAuteur = None
    unForm = FormAuteur()
    idA = int(unForm.idA.data)
    updatedAuteur = Auteur.query.get(idA)
    if unForm.validate_on_submit():
        updatedAuteur.Nom = unForm.Nom.data
        db.session.commit()
        return redirect(url_for('viewAuteur', idA=updatedAuteur.idA))
    return render_template("auteur_update.html", selectedAuteur=updatedAuteur, updateForm=unForm)

@app.route('/auteurs/<idA>/view/')
def viewAuteur(idA):
    """Détail d'un auteur"""
    unAuteur = Auteur.query.get(idA)
    unForm = FormAuteur(idA=unAuteur.idA, Nom=unAuteur.Nom)
    return render_template("auteur_view.html", selectedAuteur=unAuteur, viewForm=unForm)

@app.route('/auteur/')
def createAuteur():
    """Formulaire de création d'un auteur"""
    unForm = FormAuteur()
    return render_template("auteur_create.html", createForm=unForm)

@app.route('/auteur/insert/', methods=("POST",))
@login_required
def insertAuteur():
    """Insertion d'un nouvel auteur"""
    insertedAuteur = None
    unForm = FormAuteur()
    if unForm.validate_on_submit():
        insertedAuteur = Auteur(Nom=unForm.Nom.data)
        db.session.add(insertedAuteur)
        db.session.commit()
        return redirect(url_for('getAuteurs'))
    return render_template("auteur_create.html", createForm=unForm)

@app.route('/auteurs/<idA>/delete/')
@login_required
def deleteAuteur(idA):
    """Confirmation de suppression d'un auteur"""
    unAuteur = Auteur.query.get(idA)
    unForm = FormAuteur(idA=unAuteur.idA, Nom=unAuteur.Nom)
    return render_template("auteur_delete.html", selectedAuteur=unAuteur, deleteForm=unForm)

@app.route('/auteur/erase/', methods=("POST",))
@login_required
def eraseAuteur():
    """Suppression d'un auteur"""
    deletedAuteur = None
    unForm = FormAuteur()
    idA = int(unForm.idA.data)
    deletedAuteur = Auteur.query.get(idA)
    db.session.delete(deletedAuteur)
    db.session.commit()
    return redirect(url_for('getAuteurs'))

@app.route('/livres/')
def getLivres():
    """Liste des livres, avec recherche et tri possibles"""
    query = request.args.get("q", "").strip()
    sort_by = request.args.get("sort", "titre")

    if query:
        lesLivres = Livre.query.filter(Livre.titre.ilike(f"%{query}%"))
    else:
        lesLivres = Livre.query
    
    if sort_by == "prix_asc":
        lesLivres = lesLivres.order_by(Livre.prix.asc())
    elif sort_by == "prix_desc":
        lesLivres = lesLivres.order_by(Livre.prix.desc())
    else:
        lesLivres = lesLivres.order_by(Livre.titre)
    
    lesLivres = lesLivres.all()
    return render_template("livres_list.html", title="Les Livres", livres=lesLivres, query=query, sort_by=sort_by)

@app.route('/livres/<int:idL>/view/')
def viewLivre(idL):
    """Détail d'un livre"""
    unLivre = Livre.query.get_or_404(idL)
    unForm = FormLivre(idL=unLivre.idL, prix=unLivre.prix)
    return render_template("livre_view.html", selectedLivre=unLivre, viewForm=unForm)

@app.route('/livres/<idL>/update/')
@login_required
def updateLivre(idL):
    """Formulaire de mise à jour d'un livre"""
    unLivre = Livre.query.get(idL)
    unForm = FormLivre(idL=unLivre.idL, titre=unLivre.titre, prix=unLivre.prix)
    return render_template("livre_update.html", selectedLivre=unLivre, updateForm=unForm)

@app.route('/livre/save/', methods=("POST",))
@login_required
def saveLivre():
    """Sauvegarde les modifications d'un livre"""
    unForm = FormLivre()
    idL = int(unForm.idL.data)
    updatedLivre = Livre.query.get(idL)
    if unForm.validate_on_submit():
        updatedLivre.titre = unForm.titre.data
        updatedLivre.prix = unForm.prix.data
        db.session.commit()
        return redirect(url_for('viewLivre', idL=updatedLivre.idL))
    return render_template("livre_update.html", selectedLivre=updatedLivre, updateForm=unForm)

@app.route('/livre/create/')
@login_required
def createLivre():
    """Formulaire de création d'un livre"""
    unForm = FormLivre()
    return render_template("livre_create.html", createForm=unForm)

@app.route('/livre/insert/', methods=("POST",))
@login_required
def insertLivre():
    """Insertion d'un nouveau livre"""
    insertedLivre = None
    unForm = FormLivre()
    auteur_nom = unForm.nomA.data
    auteur = Auteur.query.filter_by(Nom=auteur_nom).first()
    image_file = unForm.img.data
    filename = None
    if image_file:
        filename = image_file.filename
        image_path = os.path.join('monApp/static/images', filename)
        image_file.save(image_path)
    if unForm.validate_on_submit():
        insertedLivre = Livre(titre=unForm.titre.data,
                              prix=unForm.prix.data,
                              url=unForm.url.data,
                              img=filename,
                              auteur=auteur)
        db.session.add(insertedLivre)
        db.session.commit()
        return redirect(url_for('getLivres'))
    return render_template("livre_create.html", createForm=unForm)


@app.route('/favoris/')
@login_required
def mesFavoris():
    """Liste des livres favoris de l'utilisateur connecté"""
    livres_favoris = current_user.favoris
    return render_template("favoris.html", title="Mes Favoris", livres=livres_favoris)

@app.route('/favoris/toggle/<int:idL>', methods=("POST",))
@login_required
def toggleFavori(idL):
    """Ajoute ou retire un livre des favoris"""
    livre = Livre.query.get_or_404(idL)
    
    if current_user.est_favori(livre):
        current_user.favoris.remove(livre)
        est_favori = False
    else:
        current_user.favoris.append(livre)
        est_favori = True
    
    db.session.commit()
    return jsonify({'success': True, 'est_favori': est_favori})

@app.route("/login/", methods=("GET", "POST",))
def login():
    """Page de login"""
    unForm = LoginForm()
    unUser = None
    if not unForm.is_submitted():
        unForm.next.data = request.args.get('next')
    elif unForm.validate_on_submit():
        unUser = unForm.get_authenticated_user()
        if unUser:
            login_user(unUser)
            next = unForm.next.data or url_for("index", name=unUser.Login)
            return redirect(next)
    return render_template("login.html", form=unForm)

@app.route("/logout/")
def logout():
    """Déconnexion de l'utilisateur"""
    logout_user()
    return redirect(url_for('index'))

@app.route("/register/", methods=("GET", "POST",))
def register():
    """Page d'inscription"""
    unForm = RegisterForm()
    newUser = None
    if unForm.validate_on_submit():
        newUser = unForm.get_registered_user()
        if newUser:
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template("register.html", form=unForm)

if __name__ == "__main__":
    app.run()