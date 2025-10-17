import os
import tempfile
import pytest
from monApp.models import User, Auteur, Livre

def test_newuser_command(testapp, caplog):
    """Test de la commande newuser"""
    with testapp.app_context():
        runner = testapp.test_cli_runner()
        result = runner.invoke(args=['newuser', 'testuser', 'testpass'])
        
        # Vérifier que la commande s'est bien exécutée
        assert result.exit_code == 0
        
        # Vérifier que l'utilisateur a été créé
        user = User.query.get('testuser')
        assert user is not None
        assert user.Login == 'testuser'

def test_newpasswrd_command_existing_user(testapp, caplog):
    """Test de la commande newpasswrd pour un utilisateur existant"""
    with testapp.app_context():
        runner = testapp.test_cli_runner()
        result = runner.invoke(args=['newpasswrd', 'CDAL', 'newpassword'])
        
        # Vérifier que la commande s'est bien exécutée
        assert result.exit_code == 0

def test_newpasswrd_command_nonexistent_user(testapp, caplog):
    """Test de la commande newpasswrd pour un utilisateur inexistant"""
    with testapp.app_context():
        runner = testapp.test_cli_runner()
        result = runner.invoke(args=['newpasswrd', 'nonexistent', 'pass'])
        
        # La commande doit retourner sans erreur (elle log juste une erreur)
        assert result.exit_code == 0

def test_syncdb_command(testapp):
    """Test de la commande syncdb"""
    with testapp.app_context():
        runner = testapp.test_cli_runner()
        result = runner.invoke(args=['syncdb'])
        
        # Vérifier que la commande s'est bien exécutée
        assert result.exit_code == 0

def test_loaddb_command(testapp):
    """Test de la commande loaddb"""
    with testapp.app_context():
        # Créer un fichier YAML temporaire
        yaml_content = """- author: Test Author
  img: test.jpg
  price: 10.0
  title: Test Book
  url: http://test.com
- author: Another Author
  img: another.jpg
  price: 15.0
  title: Another Book
  url: http://another.com
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml_content)
            temp_file = f.name
        
        try:
            runner = testapp.test_cli_runner()
            result = runner.invoke(args=['loaddb', temp_file])
            
            # Vérifier que la commande s'est bien exécutée
            assert result.exit_code == 0
            
            # Vérifier que les auteurs ont été créés
            auteurs = Auteur.query.all()
            assert len(auteurs) >= 2
            
            # Vérifier que les livres ont été créés
            livres = Livre.query.all()
            assert len(livres) >= 2
        finally:
            os.unlink(temp_file)