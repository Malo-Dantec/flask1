from flask_login import login_user
from .app import app
from flask import flash, render_template, request
from monApp.models import Auteur, Livre

@app.route('/about/')
def about():
    return render_template("about.html",title ="A propos")

@app.route('/contact/')
def contact():
    return render_template("contact.html",title ="Contact")

@app.route('/')
@app.route('/index/')
def index():
    if len(request.args)==0:
        return render_template("index.html",title="R3.01 Dev Web avec Flask",name="Cricri")
    else :
        param_name = request.args.get('name')
        return render_template("index.html",title="R3.01 Dev Web avec Flask",name=param_name)

@app.route('/auteurs/')
def getAuteurs():
    lesAuteurs = Auteur.query.all()
    return render_template('auteurs_list.html', title="Les Auteurs", auteurs=lesAuteurs)

@app.route('/livres/')
def getLivres():
    lesLivres = Livre.query.all()
    return render_template('livres_list.html', title="Les Livres", livres=lesLivres)

from monApp.forms import FormAuteur, LoginForm
from flask_login import login_required
@app.route('/auteurs/<idA>/update/')
@login_required
def updateAuteur(idA):
    unAuteur = Auteur.query.get(idA)
    unForm = FormAuteur (idA=unAuteur.idA , Nom=unAuteur.Nom)
    return render_template("auteur_update.html",selectedAuteur=unAuteur, updateForm=unForm)

from flask import url_for , redirect
from .app import db
@login_required
@app.route ('/auteur/save/', methods =("POST" ,))
def saveAuteur():
    updatedAuteur = None
    unForm = FormAuteur()
    #recherche de l'auteur à modifier
    idA = int(unForm.idA.data)
    updatedAuteur = Auteur.query.get(idA)
    #si les données saisies sont valides pour la mise à jour
    if unForm.validate_on_submit():
        updatedAuteur.Nom = unForm.Nom.data
        db.session.commit()
        return redirect(url_for('viewAuteur', idA=updatedAuteur.idA))
    return render_template("auteur_update.html",selectedAuteur=updatedAuteur, updateForm=unForm)

@app.route('/auteurs/<idA>/view/')
def viewAuteur(idA):
    unAuteur = Auteur.query.get(idA)
    unForm = FormAuteur (idA=unAuteur.idA , Nom=unAuteur.Nom)
    return render_template("auteur_view.html",selectedAuteur=unAuteur, viewForm=unForm)

@app.route('/auteur/')
def createAuteur():
    unForm = FormAuteur()
    return render_template("auteur_create.html", createForm=unForm)

@app.route ('/auteur/insert/', methods =("POST" ,))
@login_required
def insertAuteur():
    insertedAuteur = None
    unForm = FormAuteur()
    if unForm.validate_on_submit():
        insertedAuteur = Auteur(Nom=unForm.Nom.data)
        db.session.add(insertedAuteur)
        db.session.commit()
        insertedId = Auteur.query.count()
        return redirect(url_for('viewAuteur', idA=insertedId))
    return render_template("auteur_create.html", createForm=unForm)

@app.route('/auteurs/<idA>/delete/')
@login_required
def deleteAuteur(idA):
    unAuteur = Auteur.query.get(idA)
    unForm = FormAuteur(idA=unAuteur.idA, Nom=unAuteur.Nom)
    return render_template("auteur_delete.html",selectedAuteur=unAuteur, deleteForm=unForm)

@app.route ('/auteur/erase/', methods =("POST" ,))
@login_required
def eraseAuteur():
    deletedAuteur = None
    unForm = FormAuteur()
    #recherche de l'auteur à supprimer
    idA = int(unForm.idA.data)
    deletedAuteur = Auteur.query.get(idA)
    #suppression
    db.session.delete(deletedAuteur)
    db.session.commit()
    return redirect(url_for('getAuteurs'))

from monApp.forms import FormLivre

@app.route('/livres/<int:idL>/view/')
def viewLivre(idL):
    unLivre = Livre.query.get_or_404(idL)  # CORRECTION: get_or_404 pour éviter les erreurs
    unForm = FormLivre(idL=unLivre.idL, prix=unLivre.prix)
    return render_template("livre_view.html", selectedLivre=unLivre, viewForm=unForm)

@app.route('/livres/<int:idL>/update/')
@login_required
def updateLivre(idL):
    unLivre = Livre.query.get_or_404(idL)
    # CORRECTION: Pré-remplir le formulaire avec les données existantes
    unForm = FormLivre(obj=unLivre)  # obj permet de pré-remplir automatiquement
    return render_template("livre_update.html", selectedLivre=unLivre, updateForm=unForm)

@app.route('/livre/save/', methods=["POST"])
@login_required
def saveLivre():
    form = FormLivre()
    if not form.validate_on_submit():
        if form.idL.data:
            livre = Livre.query.get_or_404(int(form.idL.data))
            return render_template("livre_update.html", selectedLivre=livre, updateForm=form)
        return redirect(url_for('getLivres'))
    livre = Livre.query.get_or_404(int(form.idL.data))
    livre.prix = float(form.prix.data)
    db.session.commit()
    return redirect(url_for('viewLivre', idL=livre.idL))

@app.route ("/login/", methods =("GET","POST" ,))
def login():
    unForm = LoginForm ()
    unUser=None
    if not unForm.is_submitted():
        unForm.next.data = request.args.get('next')
    elif unForm.validate_on_submit():
        unUser = unForm.get_authenticated_user()
        if unUser:
            login_user(unUser)
            next = unForm.next.data or url_for("index",name=unUser.Login)
            return redirect (next)
    return render_template ("login.html",form=unForm)

from flask_login import logout_user
@app.route ("/logout/")
def logout():
    logout_user()
    return redirect ( url_for ('index'))


if __name__ == "__main__":
    app.run()
