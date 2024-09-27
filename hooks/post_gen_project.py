from pathlib import Path
import shutil
import secrets


TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "


def set_flag(file_path, flag, value):
    with open(file_path, "r+", encoding="utf-8") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path):
    return set_flag(
        file_path, "!!!SET DJANGO_SECRET_KEY!!!", value=secrets.token_urlsafe(32)
    )


def set_flags_in_settings_files():
    set_django_secret_key("base.py")
    set_django_secret_key("dev.py")
    set_django_secret_key("_env.dev.exemple")
    set_django_secret_key("_env.prod.exemple")


def main():
    set_flags_in_settings_files()

    packages = [
        "argon2-cffi",
        "django-environ",
        "django-extensions",
        "django-debug-toolbar",
    ]

    print(HINT + "1. Ajouter les dépedances suivante à votre projet: " + TERMINATOR)
    for package in packages:
        print(HINT + f"- {package} " + TERMINATOR)
    print()
    print(
        HINT
        + "2. Copier _env.dev.exemple ou _env.prod.exemple à la racine de votre projet et renommez-le en .env"
        + TERMINATOR
    )
    print()
    print(
        HINT
        + '3. Ajouter path("__debug__/", include("debug_toolbar.urls")) à vos urls'
        + TERMINATOR
    )
    print()
    print(
        SUCCESS
        + "Vos fichiers de configuration sont prêts ! Déplacer le répertoire settings généré dans {{ cookiecutter.config_dir | trim('\\') }} {{ cookiecutter.__config_dir }}"
        + TERMINATOR
    )
    print()
    print(
        SUCCESS
        + "Ajouter `from {{ cookiecutter.__config_dir }} import settings` dans manage.py, wsgi.py et asgi.py"
        + TERMINATOR
    )


if __name__ == "__main__":
    main()
