"""
Projet: {{ cookiecutter.project_name }}

Configuration de base commune à tous les fichiers de settings.

Pour plus d'information, la liste complète des variables de configuration est
disponible dans la doc officielle ici:
https://docs.djangoproject.com/fr/5.1/ref/settings/
"""

from pathlib import Path

from . import BASE_DIR
from . import search_dir
from . import env

# Répertoire de configuration de l'installation Django
CONFIG_DIR = search_dir(__file__, "wsgi.py", exclude_dirs=[".venv", "venv"], stop_when="manage.py")

# Répertoire des applications: {{ cookiecutter.apps_folder_name }}/
{%- if cookiecutter.apps_folder_name %}
APPS_DIR = BASE_DIR / "{{ cookiecutter.apps_folder_name }}"{% else %}
APPS_DIR = BASE_DIR{% endif %}

# ATTENTION A LA SECURITE: keep the secret key used in production secret!
# https://docs.djangoproject.com/fr/5.1/ref/settings/#std-setting-SECRET_KEY
SECRET_KEY = "!!!SET DJANGO_SECRET_KEY!!!"

# DEBUG:
# De base, on désactive le mode DEBUG pour éviter les oublis en production
# https://docs.djangoproject.com/fr/5.1/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# ALLOWED_HOSTS:
# Une liste de chaînes représentant des noms de domaine/d’hôte que ce site
# Django peut servir. C’est une mesure de sécurité pour empêcher les attaques
# d’en-tête Host HTTP, qui sont possibles même avec bien des configurations de
# serveur web apparemment sécurisées.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Applications installées sur ce projet Django
INSTALLED_APPS = [
    # Ajouter vos propres applications ...

    {%- if cookiecutter.use_wagtail %}

    # Applications venant de Wagtail
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.settings",
    "wagtail.contrib.styleguide",
    "wagtail",
    "rest_framework",
    "modelcluster",
    "taggit",{% endif %}
    # Application venant de Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # Application externes
    "django_extensions",
    {%- if cookiecutter.use_vite_for_frontend %}
    "django_vite",{% endif %}
]

# GESTION DU MUTLI-SITES
# L’ID, en tant qu’entier, du site actuel dans la table de base de données
# django_site. Cela est utilisé pour permettre aux données de l’application de
# se connecter à des sites spécifiques, et une seule base de données peut
# gérer le contenu pour plusieurs sites.
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# MIDDLEWARE:
# Les intergiciels ou middleware représentent un système de points d’entrée
# dans le traitement des requêtes et des réponses de Django. C’est un système
# de plugins léger et de bas niveau pour modifier de façon globale les
# entrées et sorties HTTP de Django.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#middleware
# Vous pouvez apprendre à écrire vos propre middlewares ici:
# https://docs.djangoproject.com/fr/5.1/topics/http/middleware/
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    {%- if cookiecutter.use_wagtail %}
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",{% endif %}
]

# URLS:
# Une chaîne représentant le chemin d’importation Python complet vers votre
# URLconf racine, par exemple "mesapplisdjango.urls".
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "!!!SET DJANGO_CONFIG_DIR!!!.urls"

# TEMPLATES:
# Une liste contenant les réglages de tous les moteurs de gabarit à utiliser
# avec Django. Chaque élément de la liste est un dictionnaire contenant les
# options de chacun des moteurs.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#templates
TEMPLATES = [
    {
        # Le moteur de gabarit à utiliser. Les moteurs de gabarit intégrés à
        # Django sont :
        # - DjangoTemplates: 'django.template.backends.django.DjangoTemplates'
        # - Jinja2: 'django.template.backends.jinja2.Jinja2'
        # https://docs.djangoproject.com/fr/5.1/ref/settings/#std-setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Répertoires dans lesquels le moteur recherche des fichiers sources de gabarits, dans
        # l’ordre de leur recherche.
        # https://docs.djangoproject.com/fr/5.1/ref/settings/#dirs
        "DIRS": [],
        # Indique si le moteur recherche des fichiers sources de gabarits dans
        # les applications installées.
        # https://docs.djangoproject.com/fr/5.1/ref/settings/#app-dirs
        "APP_DIRS": True,
        # Paramètres supplémentaires à passer au moteur de gabarit. Les paramètres disponibles
        # varient en fonction du moteur.
        "OPTIONS": {
            # Liste des processeurs de contexte. Voici ce que font chacun des processeurs de
            # contexte intégrés à Django
            # https://docs.djangoproject.com/fr/5.1/ref/templates/api/#built-in-template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

# Le chemin Python complet de l’objet application WSGI que les serveurs intégrés dans Django vont
# utiliser (par ex. runserver).
# https://docs.djangoproject.com/fr/5.1/ref/settings/#wsgi-application
WSGI_APPLICATION = "!!!SET DJANGO_CONFIG_DIR!!!.wsgi.application"


# BASE DE DONNEES:
# Un dictionnaire contenant les réglages de toutes les bases de données à
# utiliser avec Django.
# Le réglage DATABASES doit configurer une base de données default; il est possible de définir
# autant de bases de données que nécessaire.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#databases
# La configuration de cette base de données utilise ici une variable
# d'environnement sous forme d'URL nommée DJANGO_DATABASE_URL. Vous trouverez
# des exemples de telles url de configuration ici:
# - POSTGRESQL: postgres://USER:PASSWORD@HOST:PORT/DB_NAME (avec le driver psycopg)
# - MYSQL: mysql://USER:PASSWORD@HOST:PORT/DB_NAME (avec le driver mysqlclient)
# - SQLITE: sqlite:///FILE_NAME (le driver est inclus par défaut dans python)
DATABASES = {
    "default": env.db(
        "DJANGO_DATABASE_URL",
        default="sqlite:///db.sqlite3"
    )
}

# Type de champ clé primaire à utiliser par défaut pour les modèles n’ayant
# pas de champ avec primary_key=True.
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# VALIDATION DES MOTS DE PASSE
# La liste des validateurs utilisés pour vérifier la solidité des mots de passe
# des utilisateurs.
# Pour plus d'info sur la validation:
# https://docs.djangoproject.com/fr/5.1/topics/auth/passwords/#password-validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# MOTS DE PASSE
# Configuration du chiffrement des mots de passe
# https://docs.djangoproject.com/fr/5.1/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # Argon2 n’est pas l’algorithme utilisé par défaut dans Django car il
    # nécessite une bibliothèque tierce (argon2-cffi). Les experts de Password
    # Hashing Competition recommandent cependant l’utilisation immédiate de
    # Argon2 plutôt que les autres algorithmes pris en charge par Django.
    # https://docs.djangoproject.com/fr/5.1/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# INTERNATIONALISATION
# Le but de l’internationalisation et de la régionalisation est de permettre à
# une seule application web de présenter son contenu dans des langues et des
# formats adaptés à ses visiteurs.
# https://docs.djangoproject.com/fr/5.1/topics/i18n/

# Une chaîne représentant le code de langue de cette installation. Elle
# doit respecter le format de langue standard.
# Par exemple, l’anglais des États-Unis est “en-us” ou le français est “fr”.
# Vous pouvez aussi voir la liste des identifiants de langue ici:
# http://www.i18nguy.com/unicode/language-identifiers.html
# La doc pour LANGUAGE_CODE se trouve ici.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#std-setting-LANGUAGE_CODE
LANGUAGE_CODE = "{{ cookiecutter.language }}"

# Une chaîne représentant le fuseau horaire pour cette installation.
# 'America/Chicago' est la valeur par défaut, mais le settings de départ
# utilise souvent la valeur 'UTC'.
# Vous trouvez une liste des fuseau horaires ici:
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
# Pour Paris, vous pouvez par exemple utiliser la valeur 'Europe/Paris'
TIME_ZONE = "{{ cookiecutter.timezone }}"

# Une valeur booléenne indiquant si le système de traduction de Django doit
# être activé. C’est un moyen de le désactiver pour gagner un peu de
# performances. Si défini à False, Django optimise son fonctionnement pour ne
# pas charger le mécanisme de traduction.
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# Une valeur booléenne indiquant si les dates/heures sont conscientes de leur
# fuseau horaire. Si défini à True, Django utilise en interne des dates/heures
# conscientes de leur fuseau horaire.
# Lorsque USE_TZ vaut False, Django utilise des dates/heures naïves en temps
# local, sauf si des dates mises en forme en ISO 8601 et contenant un fuseau
# horaire sont interprétées ; dans ce cas, le fuseau horaire est conservé.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#std-setting-USE_TZ
USE_TZ = True

# AUTHENTIFICATION DES UTILISATEURS
# Une liste de classes de moteurs d’authentification (sous forme de chaînes)
# à utiliser durant la tentative d’authentification d’un utilisateur.
# Consultez la documentation sur les moteurs d’authentification pour plus de
# détails.
# https://docs.djangoproject.com/fr/5.1/topics/auth/customizing/#other-authentication-sources
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Le modèle à utiliser pour représenter un utilisateur. Voir Substitution par
# un modèle User personnalisé.
# https://docs.djangoproject.com/fr/5.1/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = "{{ cookiecutter.user_model }}"

{%- if cookiecutter.login_redirect_url %}

# L’URL ou le motif d’URL nommé vers lequel seront redirigées les requêtes
# après la connexion si la vue LoginView ne reçoit pas de paramètre GET next:
# https://docs.djangoproject.com/fr/5.1/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "home"{% endif %}

{%- if cookiecutter.logout_redirect_url %}

# L’URL ou le motif d’URL nommé vers lequel seront redirigées les requêtes
# après la déconnexion si la vue LogoutView ne possède pas d’attribut next_page.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#logout-redirect-url
LOGOUT_REDIRECT_URL = "home"{% endif %}

# L’URL ou le motif d’URL nommé vers lequel seront redirigées les requêtes
# pour la connexion avec le décorateur login_required(), les classes
# LoginRequiredMixin, AccessMixin ou quand le middleware
# LoginRequiredMiddleware est installé.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#login-url
LOGIN_URL = "{{ cookiecutter.login_url }}"

# FICHIERS STATIQUES ET MEDIA (CSS, JavaScript, Images)
# Les sites Web ont généralement besoin de servir des fichiers supplémentaires
# tels que des images, du JavaScript ou du CSS. Dans Django, ces fichiers
# sont appelés « fichiers statiques ». Django met à disposition l'app
# django.contrib.staticfiles pour vous assister dans cette gestion.
# https://docs.djangoproject.com/fr/5.1/howto/static-files/

# Le chemin absolu vers le répertoire dans lequel collectstatic rassemble les fichiers statiques en
# vue du déploiement.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#static-root
STATIC_ROOT = BASE_DIR / "staticfiles"

# URL utilisée pour se référer aux fichiers statiques se trouvant dans
# STATIC_ROOT.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#static-url
STATIC_URL = "/static/"

# Ce réglage définit les emplacements supplémentaires que l’application
# staticfiles parcourt.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#staticfiles-dirs
STATICFILES_DIRS = []

# La configuration STORAGES définit les backends de stockage pour les fichiers
# par défaut et les fichiers statiques dans une application Django.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#storages
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Liste des moteurs de découverte sachant retrouver les fichiers statiques
# en divers endroits.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# FICHIERS DE MEDIA

# Chemin absolu de répertoire pointant vers le répertoire qui contiendra les
# fichiers uploadés par les utilisateurs.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#media-root
MEDIA_ROOT = APPS_DIR / "media"

# URL qui gère les fichiers médias servis à partir de MEDIA_ROOT, utilisée pour
# la gestion des fichiers stockés. Elle doit se terminer par une barre oblique
# si elle ne contient pas de valeur vide.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#media-url
MEDIA_URL = "/media/"

# SECURITE
# Indique si le drapeau HttpOnly doit être utilisé sur le cookie de session.
# Si ce paramètre est défini à True, le code JavaScript côté client ne sera
# pas en mesure d’accéder au cookie de session.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True

# Indique si le drapeau HttpOnly doit être utilisé sur le cookie CSRF. Si ce
# paramètre est défini à True, le JavaScript côté client ne sera pas en mesure
# d’accéder au cookie CSRF.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True

# Valeur par défaut de l’en-tête X-Frame-Options utilisé par
# XFrameOptionsMiddleware pour se protéger contre le
# détournement de click (clickjacking)
# https://docs.djangoproject.com/fr/5.1/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# Configuration de l'email. Par défaut, les courriels sont affichés dans le
# le terminal.
# Pour définir un back-end d'envoi d'emails, définir la variable d'environnement
# DJANGO_EMAIL_URL avec les valeurs suivantes:
# - SMTP avec SSL: smtp+ssl://USER:PASSWORD@HOST:PORT
# - SMTP avec STARTTLS: smtp+tls://USER:PASSWORD@HOST:PORT
# - Console: consolemail://
# https://docs.djangoproject.com/fr/5.1/ref/settings/
EMAIL_CONFIG = env.email(
    "DJANGO_EMAIL_URL",
    default="consolemail://",
)
globals().update(**EMAIL_CONFIG)

# Définit un délai d’expiration en secondes pour des opérations bloquantes
# telles que la tentative de connexion.
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# EMAILS D'ADMIN
# Une liste de toutes les personnes qui reçoivent les notifications d’erreurs
# dans le code. Lorsque DEBUG=False et que AdminEmailHandler est configuré
# dans LOGGING (comportement par défaut), Django envoie un courriel à ces
# personnes contenant les détails des exceptions produites dans le cycle
# requête/réponse.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#admins
ADMINS = [
    ("""{{ cookiecutter.author_name }}""", "{{ cookiecutter.email }}")
]

# Une liste dans le même format que ADMINS qui détermine qui doit recevoir
# les notifications de liens brisés lorsque BrokenLinkEmailsMiddleware est
# activé.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING OU JOURNALISATION
# Dictionnaire de configuration de la journalisation.
# Il est possible de consulter les valeurs par défaut ici:
# https://github.com/django/django/blob/main/django/utils/log.py
# https://docs.djangoproject.com/fr/5.1/ref/settings/#logging
# Voir aussi https://docs.djangoproject.com/fr/5.1/topics/logging/ pour plus
# de détails au sujet de la configuration de la journalisation.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

{%- if cookiecutter.use_wagtail %}

# CONFIGURATION DE WAGTAIL

# Use Elasticsearch as the search backend for extra performance and better search results
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
        "INDEX": "db.sqlite3",
    },
}

WAGTAIL_SITE_NAME = "wagtaildemo"{% endif %}
