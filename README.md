## Malo DANTEC - 2A3

## Base de données

Charger la bd :
```bash
flask loaddb monApp/data/data.yml
```

Synchroniser la bd :
```bash
flask syncdb
```

## Dépendances

Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Lancer l'application

```bash
flask run
```

## Utilisateur

Ajouter un utilisateur :
```bash
flask newuser <nom> <mdp>
```

Modifier le mdp d'un utilisateur :
```bash
flask newpasswrd <nom> <mdp>
```

## Tests

Lancer les tests :
```bash
coverage run -m pytest
```

Rapport de tests dans le terminal :
```bash
coverage report -m
```

Rapport de tests HTML :
```bash
coverage html
```