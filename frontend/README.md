# Interface de démonstration

Depuis la racine du dépôt :

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r frontend/requirements.txt
uvicorn frontend.app.main:app --reload --port 3001
```

Ouvrir http://localhost:3001.

Pages disponibles : `/login`, `/code-gmail`, `/rh`, `/it`.
Les templates héritent de `app/templates/base.html`. Le style commun se trouve
 dans `app/static/style.css` et les interactions dans `app/static/app.js`.

Les formulaires sont des démonstrations : aucune donnée n’est envoyée ni stockée.
Le code e-mail n’est ni envoyé ni vérifié. Les espaces RH et informatique sont des
aperçus publics sans données réelles ; le backend devra vérifier l’authentification
et les rôles avant de les connecter à des services. Les cartes « À venir » ne sont
pas encore des fonctionnalités disponibles.

Le fichier Docker Compose existant utilise encore Node pour le frontend ; utiliser
la commande Python ci-dessus pour cette interface FastAPI. 
