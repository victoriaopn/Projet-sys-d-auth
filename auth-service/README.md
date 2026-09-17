# SSO DGFiP — Partie P2 (Auth core)

## Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer le serveur

```bash
uvicorn app.main:app --reload
```

Puis ouvrir http://127.0.0.1:8000/docs pour tester `/register` et `/login` directement dans Swagger.

## Ce qui est fait (P2)

- `POST /register` — création de compte, hash bcrypt, validation du mot de passe (12 car. min, majuscule, chiffre, spécial)
- `POST /login` — vérifie les identifiants, pose deux cookies HttpOnly : `access_token` (JWT, 15 min) et `refresh_token` (7 jours)
- `POST /refresh-token` — génère un nouvel access token à partir du refresh token
- `POST /logout` — révoque le refresh token en base et supprime les cookies
- `GET /users/me` — exemple de route protégée par `get_current_user`
- `get_current_user` (dans `app/auth.py`) — dépendance FastAPI réutilisable par toute l'équipe pour protéger n'importe quelle route :

```python
from app.auth import get_current_user

@router.get("/ma-route-protegee")
def ma_route(current_user: User = Depends(get_current_user)):
    ...
```

## Pour la suite du groupe

- **P3** : le champ `role` existe déjà sur `User` et dans le payload JWT (`payload["role"]`) → sert de base au RBAC
- **P4** : les routes `/register` et `/login` sont fonctionnelles, à brancher sur les formulaires Jinja2
- **P5** : le login réussi/échoué se passe dans `login()` (`app/routers/auth_routes.py`) → bon endroit pour écrire dans `connection_logs`

## À ne pas oublier avant la soutenance

- `SECRET_KEY` dans `app/auth.py` est en dur → à sortir en variable d'environnement
- `secure=True` sur les cookies dès que vous êtes en HTTPS
