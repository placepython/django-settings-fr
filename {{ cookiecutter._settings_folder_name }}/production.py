"""
Projet: {{ cookiecutter.project_name }}

Configuration de production.

Pour plus d'information, la liste complète des variables de configuration est
disponible dans la doc officielle ici:
https://docs.djangoproject.com/fr/5.1/ref/settings/
"""

from .base import *  # noqa: F403
from .base import MIDDLEWARE
from .base import STORAGES
from .base import env

# GENERAL
# ATTENTION A LA SECURITE: la clé secrète utilisée en production est une donnée
# sensible.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#std-setting-SECRET_KEY
SECRET_KEY = env("DJANGO_SECRET_KEY")

# DEBUG:
# SECURITY WARNING: keep the secret key used in production secret!
# https://docs.djangoproject.com/fr/5.1/ref/settings/#std-setting-SECRET_KEY
DEBUG = env.bool("DJANGO_DEBUG", False)

# ALLOWED HOSTS
# Une liste de chaînes représentant des noms de domaine/d’hôte que ce site
# Django peut servir. C’est une mesure de sécurité pour empêcher les attaques
# d’en-tête Host HTTP, qui sont possibles même avec bien des configurations de
# serveur web apparemment sécurisées.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["{{ cookiecutter.domain_name }}"])

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
    "default": env.db("DJANGO_DATABASE_URL")
}

# CONN_MAX_AGE est utilisé dans une configuration de production Django pour
# définir la durée pendant laquelle les connexions à la base de données sont
# réutilisées, ce qui permet d'améliorer les performances en réduisant le coût
# de création de nouvelles connexions à chaque requête.
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

{%- if cookiecutter.deployment_platform == "VPS" and cookiecutter.use_redis %}

# CACHES
# Cette configuration CACHES avec Redis en production permet à Django
# d'utiliser Redis comme backend de cache.
# https://docs.djangoproject.com/fr/5.1/topics/cache/#redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL", default="http:/127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
            "IGNORE_EXCEPTIONS": True,
        },
        "KEY_PREFIX": "{{ cookiecutter.author_name.lower() | trim() |replace(' ', '_') }}"
    },
}

# La configuration SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# indique à Django d'utiliser le backend de cache configuré pour stocker les
# sessions, ce qui peut améliorer la performance en stockant les sessions en
# mémoire ou dans un système de cache comme Redis.
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
{% else %}

# CACHES
# Pour en savoir plus sur l'usage du framework de cache de Django:
# https://docs.djangoproject.com/fr/5.1/topics/cache/
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    },
}{% endif %}

# SECURITE
# La variable SECURE_PROXY_SSL_HEADER est utilisée dans Django pour indiquer
# que l'application est derrière un proxy inverse (comme Nginx ou un load
# balancer) qui gère le protocole SSL. En définissant
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https"), on spécifie à
# Django de considérer les requêtes avec l'en-tête HTTP_X_FORWARDED_PROTO comme
# sécurisées si elles sont marquées avec la valeur "https".
# Cela permet à Django de traiter correctement ces requêtes comme étant faites
# via HTTPS, même si la connexion entre Django et le proxy est en HTTP.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# La variable SECURE_SSL_REDIRECT configure Django pour rediriger
# automatiquement toutes les requêtes HTTP vers HTTPS
# https://docs.djangoproject.com/fr/5.1/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)

# La variable SESSION_COOKIE_SECURE = True garantit que les cookies de session
# ne sont envoyés que via des connexions HTTPS, renforçant ainsi la sécurité en
# empêchant leur transmission sur des connexions non sécurisées.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True

# La variable SESSION_COOKIE_NAME = "__Secure-sessionid" permet de définir un
# nom personnalisé pour le cookie de session, et le préfixe __Secure- est
# souvent utilisé pour indiquer que ce cookie doit être envoyé uniquement sur
# des connexions HTTPS.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#session-cookie-name
SESSION_COOKIE_NAME = "__Secure-sessionid"

# La variable CSRF_COOKIE_SECURE = True garantit que le cookie CSRF (utilisé
# pour protéger contre les attaques CSRF) n'est transmis que via des connexions
# HTTPS, renforçant ainsi la sécurité des requêtes contre les attaques sur des
# connexions non sécurisées.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

# La variable CSRF_COOKIE_NAME = "__Secure-csrftoken" personnalise le nom du
# cookie CSRF, et le préfixe __Secure- est utilisé pour indiquer que le cookie
# doit être envoyé uniquement sur des connexions HTTPS, conformément aux
# meilleures pratiques de sécurité pour les cookies sensibles.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#csrf-cookie-name
CSRF_COOKIE_NAME = "__Secure-csrftoken"

# La variable SECURE_HSTS_SECONDS = 60 active la politique HTTP Strict
# Transport Security (HSTS) pour 60 secondes, demandant aux navigateurs
# d'utiliser exclusivement des connexions HTTPS pour le site pendant cette
# durée, renforçant ainsi la sécurité en empêchant les dégradations vers HTTP.
# https://docs.djangoproject.com/fr/5.1/topics/security/#ssl-https
# https://docs.djangoproject.com/fr/5.1/ref/settings/#secure-hsts-seconds
# TODO: Réglez d'abord cette valeur à 60 secondes, puis à 518400 une fois que
# vous aurez prouvé que la première fonctionne.
SECURE_HSTS_SECONDS = 60

# La variable SECURE_HSTS_INCLUDE_SUBDOMAINS indique si la politique HSTS
# (HTTP Strict Transport Security) doit s'appliquer également à tous les
# sous-domaines du site. En la configurant avec une variable d'environnement,
# ici par défaut à True, elle garantit que toutes les requêtes vers les
# sous-domaines doivent aussi être forcées à utiliser HTTPS, renforçant ainsi
# la sécurité à l'échelle de l'ensemble du domaine.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=True,
)

# La variable SECURE_HSTS_PRELOAD, lorsqu'elle vaut True, permet au domaine
# d'être inscrit dans la liste de préchargement HSTS. Cela signifie que les
# navigateurs qui supportent cette fonctionnalité refuseront toute connexion
# HTTP dès la première visite, renforçant ainsi la sécurité en évitant les
# attaques avant même la première requête HTTP non sécurisée.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)

# La variable SECURE_CONTENT_TYPE_NOSNIFF, activée ici par défaut via une
# variable d'environnement, permet d'ajouter l'en-tête HTTP
# X-Content-Type-Options: nosniff aux réponses. Cet en-tête empêche les
# navigateurs de deviner le type de contenu et de le traiter différemment de
# celui spécifié, ce qui renforce la sécurité en empêchant certaines attaques,
# comme celles liées aux types de fichiers mal interprétés (MIME type sniffing).
# https://docs.djangoproject.com/fr/5.1/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF",
    default=True,
)


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

# La variable DEFAULT_FROM_EMAIL définit l'adresse email par défaut utilisée
# par Django pour envoyer des emails depuis l'application.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="{{cookiecutter.project_name}} <noreply@{{cookiecutter.domain_name}}>",
)

# La variable SERVER_EMAIL définit l'adresse email utilisée pour envoyer des
# messages d'erreur ou d'alerte émanant du serveur Django, comme les
# notifications d'erreurs 500.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

# La variable EMAIL_SUBJECT_PREFIX ajoute un préfixe personnalisé aux sujets de
# tous les emails envoyés par l'application Django.
# https://docs.djangoproject.com/fr/5.1/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[{{cookiecutter.project_name}}] ",
)

# ADMIN
# La variable ADMIN_URL définit l'URL personnalisée pour accéder à l'interface
# d'administration Django. En la configurant via une variable d'environnement,
# cela permet de masquer ou de rendre l'URL de l'administration moins
# prévisible (au lieu de l'URL par défaut /admin/), améliorant ainsi la
# sécurité en réduisant le risque d'attaques automatisées sur l'interface
# d'administration.
ADMIN_URL = env("DJANGO_ADMIN_URL")


# Journalisation
# https://docs.djangoproject.com/fr/5.1/ref/settings/#logging
# Voir https://docs.djangoproject.com/fr/5.1/topics/logging/
# pour plus de détails sur la personnalisation de la configuration du logging.
# Un exemple de configuration de logging. La seule action de logging
# concrète effectuée par cette configuration est d'envoyer un email
# aux administrateurs du site pour chaque erreur HTTP 500 lorsque DEBUG=False.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}

{%- if cookiecutter.use_vite_for_frontend %}

# La configuration DJANGO_VITE permet d'intégrer Vite, un bundler JavaScript,
# avec Django. Ici, le paramètre dev_mode est défini en fonction de la variable
# DEBUG, ce qui signifie que, lorsque DEBUG est activé (mode développement),
# Vite fonctionne en mode de développement pour un rechargement rapide et le
# hot-reloading des fichiers frontend.
# https://github.com/MrBin99/django-vite/blob/master/README.md
DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
    },
}{% endif %}
