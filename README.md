

Charger la bd :
```
flask loaddb monApp/data/data.yml
```
Ajouter la table User :
```
flask syncdb
```

Installer les dépendances :
```
pip install -r requirements.txt
```

Ajouter un utilisateur :
```
flask newuser <nom> <mdp>
```

Modifier le mdp d'un utilisateur :
```
flask newpasswrd <nom> <mdp>
```