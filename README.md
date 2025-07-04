# Journal du Développeur — API

> API RESTful pour la gestion des snippets de code personnalisés
> Permet à chaque utilisateur d'organiser, créer, modifier, supprimer et consulter ses propres snippets, catégories, tags, et langages.

---

## Table des matières

* [Présentation](#présentation)
* [Technologies](#technologies)
* [Installation](#installation)
* [Configuration](#configuration)
* [Endpoints principaux](#endpoints-principaux)
* [Authentification](#authentification)
* [Modèles et relations](#modèles-et-relations)
* [Exemples d’utilisation](#exemples-dutilisation)
* [Tests](#tests)
* [Contribuer](#contribuer)
* [Licence](#licence)

---

## Présentation

Cette API Django REST Framework permet de gérer un journal personnel de snippets de code. Chaque utilisateur peut :

* Créer, modifier, supprimer ses snippets
* Organiser les snippets avec des catégories et tags personnalisés
* Associer un langage de programmation à chaque snippet
* Restreindre l’accès aux snippets uniquement à leur propriétaire

---

## Technologies

* Python 3.11+
* Django 4.x
* Django REST Framework
* JWT (via djangorestframework-simplejwt) pour l’authentification
* Pytest pour les tests

---

## Installation

```bash
git clone https://github.com/jeanronald22/snippet-manager.git
cd snippet-manager
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Configuration

* Configure les variables d’environnement (ex : SECRET\_KEY, DB settings, etc) dans `.env`
* Assure-toi que l’endpoint `/api/auth/token/` est actif pour récupérer les tokens JWT

---

## Endpoints principaux

| Endpoint                   | Méthode              | Description                                  | Authentification requise |
| -------------------------- | -------------------- | -------------------------------------------- | ------------------------ |
| `/api/auth/token/`         | POST                 | Récupérer un token JWT (login)               | Non                      |
| `/api/auth/token/refresh/` | POST                 | Rafraîchir un token JWT                      | Non                      |
| `/api/languages/`          | GET,POST             | Lister / créer des langages                  | Oui                      |
| `/api/languages/{id}/`     | GET,PUT,PATCH,DELETE | Détails / modifier / supprimer un langage    | Oui                      |
| `/api/categories/`         | GET,POST             | Lister / créer des catégories                | Oui                      |
| `/api/categories/{id}/`    | GET,PUT,PATCH,DELETE | Détails / modifier / supprimer une catégorie | Oui                      |
| `/api/tags/`               | GET,POST             | Lister / créer des tags                      | Oui                      |
| `/api/tags/{id}/`          | GET,PUT,PATCH,DELETE | Détails / modifier / supprimer un tag        | Oui                      |
| `/api/snippets/`           | GET,POST             | Lister / créer des snippets                  | Oui                      |
| `/api/snippets/{id}/`      | GET,PUT,PATCH,DELETE | Détails / modifier / supprimer un snippet    | Oui                      |

* documentation complete `/redoc/` ou `/swagger/` une fois le projet lancer
---

## Authentification

Cette API utilise **JSON Web Tokens (JWT)** pour sécuriser l’accès.
Pour se connecter, envoyer un POST à `/api/auth/token/` avec :

```json
{
  "username": "ton_user",
  "password": "ton_mdp"
}
```

En réponse, tu recevras un access token à passer dans le header `Authorization` :

```
Authorization: Bearer <token>
```
Et un refresh pour le rafraichissement du token d'accès

---

## Exemples d’utilisation

### Créer un snippet

```http
POST /api/snippets/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Afficher un message",
  "description": "Exemple simple en Python",
  "code": "print('Hello world')",
  "instruction": "Utilise ce snippet pour afficher du texte.",
  "categories": [1],
  "tags": [3, 4],
  "language": 2
}
```

---

## Tests

Utilise `pytest` pour exécuter les tests unitaires et d’intégration :

```bash
pytest
```

Les tests couvrent la gestion des snippets, catégories, tags, langages, ainsi que les règles de sécurité liées à l’utilisateur.

---

## Contribuer

Merci de contribuer au projet !
Forke, crée une branche feature, puis fais une Pull Request.

---

## Licence

[MIT License](./LICENSE)

