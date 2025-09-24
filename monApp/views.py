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

from monApp.forms import FormAuteur
@app.route('/auteurs/<idA>/update/')
def updateAuteur(idA):
    unAuteur = Auteur.query.get(idA)
    unForm = FormAuteur(idA=unAuteur.idA , Nom=unAuteur.Nom)
    return render_template("auteur_update.html",selectedAuteur=unAuteur, updateForm=unForm)

from flask import url_for , redirect
from .app import db
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
def deleteAuteur(idA):
    unAuteur = Auteur.query.get(idA)
    unForm = FormAuteur(idA=unAuteur.idA, Nom=unAuteur.Nom)
    return render_template("auteur_delete.html",selectedAuteur=unAuteur, deleteForm=unForm)

@app.route ('/auteur/erase/', methods =("POST" ,))
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
def updateLivre(idL):
    unLivre = Livre.query.get_or_404(idL)
    # CORRECTION: Pré-remplir le formulaire avec les données existantes
    unForm = FormLivre(obj=unLivre)  # obj permet de pré-remplir automatiquement
    return render_template("livre_update.html", selectedLivre=unLivre, updateForm=unForm)

@app.route('/livre/save/', methods=["POST"])
def saveLivre():
    print("DEBUG: Route saveLivre appelée")
    unForm = FormLivre()
    
    # Debug des données reçues
    print(f"DEBUG: request.form = {request.form}")
    print(f"DEBUG: unForm.idL.data = {unForm.idL.data}")
    print(f"DEBUG: unForm.prix.data = {unForm.prix.data}")
    
    # Vérifier si le formulaire est valide
    is_valid = unForm.validate_on_submit()
    print(f"DEBUG: Formulaire valide? {is_valid}")
    
    if not is_valid:
        print(f"DEBUG: Erreurs de validation: {unForm.errors}")
        # Si pas valide, on doit récupérer le livre quand même pour réafficher le formulaire
        if unForm.idL.data:
            try:
                idL = int(unForm.idL.data)
                updatedLivre = Livre.query.get_or_404(idL)
                return render_template("livre_update.html", selectedLivre=updatedLivre, updateForm=unForm)
            except:
                return redirect(url_for('getLivres'))
        else:
            return redirect(url_for('getLivres'))
    
    # Si le formulaire est valide
    try:
        idL = int(unForm.idL.data)
        print(f"DEBUG: ID du livre à modifier: {idL}")
        
        updatedLivre = Livre.query.get_or_404(idL)
        print(f"DEBUG: Livre trouvé: {updatedLivre}")
        print(f"DEBUG: Ancien prix: {updatedLivre.prix}")
        
        # Modifier le prix
        nouveau_prix = float(unForm.prix.data)
        updatedLivre.prix = nouveau_prix
        print(f"DEBUG: Nouveau prix: {nouveau_prix}")
        
        # Sauvegarder
        db.session.commit()
        print("DEBUG: Sauvegarde réussie dans la base")
        
        # Redirection vers la vue du livre
        print(f"DEBUG: Redirection vers viewLivre avec idL={updatedLivre.idL}")
        return redirect(url_for('viewLivre', idL=updatedLivre.idL))
        
    except ValueError as e:
        print(f"DEBUG: Erreur de conversion: {e}")
        db.session.rollback()
        return redirect(url_for('getLivres'))
    except Exception as e:
        print(f"DEBUG: Erreur générale: {e}")
        db.session.rollback()
        return redirect(url_for('getLivres'))



if __name__ == "__main__":
    app.run()
