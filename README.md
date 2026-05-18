# Adra Diallo — Site de campagne FRONDEG Liste Nationale 2026

Site de campagne pour **Abdourahamane « Adra » Diallo**, candidat FRONDEG sur la **liste nationale** aux élections législatives guinéennes du **24 mai 2026**.

## Stack technique

| Composant          | Technologie                                            |
| ------------------ | ------------------------------------------------------ |
| Backend            | Django 6 + Jazzmin                                     |
| Hébergement        | Vercel (serverless Python 3.12)                        |
| Base de données    | Supabase — PostgreSQL (Transaction pooler, port 6543)  |
| Stockage médias    | Supabase Storage S3 (upload direct navigateur)         |
| Fichiers statiques | WhiteNoise + collectstatic                             |

## Démarrage rapide

```bash
git clone <repo> adra-diallo
cd adra-diallo

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# PostgreSQL local
psql -U postgres -c "CREATE USER adra_user WITH PASSWORD 'adra2026';"
psql -U postgres -c "CREATE DATABASE adra_diallo_dev OWNER adra_user;"

cp .env.example .env   # adapter si nécessaire

python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

Le site est accessible sur `http://localhost:8000` et l'admin sur `http://localhost:8000/admin`.

## Variables d'environnement

Copier `.env.example` en `.env` et renseigner les valeurs. En développement local, `USE_S3=False` suffit — les médias sont stockés dans `media/` (ignoré par git).

Pour la production (Vercel), définir les variables dans le tableau de bord Vercel :

```ini
SECRET_KEY, DEBUG, ALLOWED_HOSTS
DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
USE_S3, SUPABASE_S3_KEY_ID, SUPABASE_S3_SECRET
SUPABASE_S3_ENDPOINT, SUPABASE_S3_REGION, SUPABASE_BUCKET
```

## Commandes utiles

```bash
# Charger les données initiales (publications, programme, parcours…)
python manage.py seed_data

# Configurer le CORS S3 (une seule fois après déploiement, avec USE_S3=True)
python manage.py set_s3_cors

# Migrations production (depuis la machine locale, credentials Supabase en env)
python manage.py migrate
```

## Structure du projet

```text
adra_diallo/          ← settings, urls, wsgi
campaign/
├── models.py         ← SiteSettings, HeroSlide, BioDimension, TimelineStep,
│                        ProgramAxis, Commitment, KeyStat, Publication,
│                        ComparativeAnalysis, ComparisonPoint, NewsArticle
├── admin.py          ← Interface Jazzmin en français
├── views.py          ← index, presign_upload, publications_json
├── forms.py / widgets.py  ← upload direct S3
└── management/commands/
    ├── seed_data.py
    └── set_s3_cors.py
templates/campaign/index.html  ← SPA (12 sections)
static/
├── css/main.css      ← Palette rouge/or/vert guinéenne, Libre Baskerville
├── js/main.js
└── admin/js/s3_direct_upload.js
```

## Sections du site

1. **Hero** — Carousel photos + slogan + boutons
2. **Chiffres clés** — Compteurs animés
3. **Double Portrait** — Dimension intellectuelle / dimension sociale
4. **Parcours** — Timeline académique et professionnelle
5. **Programme** — 5 axes législatifs
6. **Publications académiques** — Filtrées par catégorie
7. **Analyse comparative Doumbouya** — Tableau promesse / réalité
8. **Actualités** — Articles de campagne
9. **Engagements** — Contrat citoyen
10. **Contact / Rejoindre** — Formulaire d'inscription
11. **Footer**

## URLs de déploiement

| URL                              | Description                                          |
| -------------------------------- | ---------------------------------------------------- |
| `https://adradiallo.frondeg.co`  | Domaine candidat                                     |
| `https://adra-diallo.vercel.app` | URL Vercel de secours                                |
| `/admin`                         | Interface d'administration                           |
| `/api/publications/`             | API JSON publications (filtre `?category=academic`)  |
