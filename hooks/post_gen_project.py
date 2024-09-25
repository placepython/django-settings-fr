from pathlib import Path
import shutil
import secrets


TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

def search_dir(from_dir, *items, exclude_dirs=None, stop_when=None, max_parents=None):
    """
    Recursively searches for specified items (files or directories) starting from the given directory
    and its parent directories, up to a specified limit of parent levels. If one of the stop conditions
    is met, the search halts.

    Parameters:
    - from_dir (str or Path): The starting directory to begin the search.
    - *items (str): The names of files or directories to search for.
    - exclude_dirs (str or list, optional): Directory or directories to exclude from the search.
    - stop_when (str or list, optional): A file or directory name (or list of names) that,
      if found, stops the upward traversal of directories.
    - max_parents (int, optional): The maximum number of parent directories to search through.
      If None, it will traverse all the way to the root.

    Returns:
    - Path or None: If an item is found, returns the absolute path of the directory containing it
      (or the directory itself if the item is a directory). If no item is found, returns None.
    """

    # Convert from_dir to Path and resolve it to an absolute path
    start_path = Path(from_dir).resolve(strict=True)

    # If exclude_dirs is a string, convert it to a list
    if isinstance(exclude_dirs, str):
        exclude_dirs = [exclude_dirs]
    elif exclude_dirs is None:
        exclude_dirs = []

    # If stop_when is a string, convert it to a list
    if isinstance(stop_when, str):
        stop_when = [stop_when]
    elif stop_when is None:
        stop_when = []

    # Function to check if a directory is in the exclude list
    def is_excluded(directory):
        return any(exclude in str(directory) for exclude in exclude_dirs)

    # Function to search a directory and its subdirectories for the items
    def search_in_directory(directory):
        if is_excluded(directory):
            return None

        # Traverse the directory and its subdirectories
        for child in directory.rglob('*'):
            if is_excluded(child.parent):
                continue
            # If an item is found, return the parent directory if it's a file, or the item itself if it's a directory
            if child.name in items:
                return child.parent.resolve(strict=True) if child.is_file() else child.resolve(strict=True)
        return None

    # Function to check if the stop_when condition is met in the directory
    def check_stop_condition(directory):
        for stop_item in stop_when:
            if (directory / stop_item).exists():
                return True
        return False

    # Traverse from from_dir and its parent directories
    parents_list = [start_path] + list(start_path.parents)

    # If max_parents is specified, limit the number of parent directories to search
    if max_parents is not None:
        parents_list = parents_list[:max_parents + 1]  # Include the start directory plus max_parents levels

    for directory in parents_list:
        # First, search the current directory and its children
        result = search_in_directory(directory)
        if result:
            return result

        # Check if the stop condition is met
        if check_stop_condition(directory):
            print(f"Stopping traversal: One of the stop_when items found in {directory}")
            break

    return None


CONFIG_DIR = search_dir(
    '__init__.py',
    "wsgi.py",
    exclude_dirs=[".venv", "venv"],
    stop_when="manage.py"
)

BASE_DIR = search_dir(
    'manage.py',
    exclude_dirs=[".venv", "venv"],
    stop_when="manage.py"
)


def set_flag(file_path, flag, value=None):
    if value is None:
        value = secrets.token_hex(64)

    with open(file_path, "r+", encoding="utf-8") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path):
    return set_flag(file_path, "!!!SET DJANGO_SECRET_KEY!!!",)

def set_django_config_path(file_path, value):
    return set_flag(file_path, "!!!SET DJANGO_CONFIG_DIR!!!", value=value)

def set_flags_in_settings_files():
    set_django_config_path("_env.dev.exemple", CONFIG_DIR.name)
    set_django_config_path("_env.prod.exemple", CONFIG_DIR.name)
    set_django_config_path("base.py", CONFIG_DIR.name)
    set_django_config_path("dev.py", CONFIG_DIR.name)
    set_django_config_path("production.py", CONFIG_DIR.name)
    set_django_secret_key("base.py")
    set_django_secret_key("dev.py")
    set_django_secret_key("production.py")
    set_django_secret_key("_env.dev.exemple")
    set_django_secret_key("_env.prod.exemple")

def main():
    set_flags_in_settings_files()

    settings_file = CONFIG_DIR / "settings.py"
    if settings_file.exists():
        settings_file.rename(settings_file.with_name("settings.py.backup"))

    settings_dir = CONFIG_DIR / "settings"
    if settings_dir.exists():
        settings_dir.rename(settings_dir.with_name("settings.backup"))

    with open(Path("../manage.py"), "r+", encoding="utf-8") as f:
        file_contents = f.read()
        file_contents = file_contents.replace(
            "import os\nimport sys",
            f"import os\nimport sys\n\nfrom {CONFIG_DIR.name} import settings # noqa: F401"
        )
        file_contents = file_contents.replace(
            '"config.settings"',
            '"config.settings.dev"'
        )
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    wsgi_file = CONFIG_DIR / "wsgi.py"
    if wsgi_file.exists():
        with open(wsgi_file, "r+", encoding="utf-8") as f:
            file_contents = f.read()
            file_contents = file_contents.replace(
                "from django.core.wsgi import get_wsgi_application",
                f"from django.core.wsgi import get_wsgi_application\n\nfrom . import settings # noqa: F401"
            )
            file_contents = file_contents.replace(
                '"config.settings"',
                '"config.settings.dev"'
            )
            f.seek(0)
            f.write(file_contents)
            f.truncate()

    asgi_file = CONFIG_DIR / "asgi.py"
    if asgi_file.exists():
        with open(asgi_file, "r+", encoding="utf-8") as f:
            file_contents = f.read()
            file_contents = file_contents.replace(
                "from django.core.asgi import get_asgi_application",
                f"from django.core.asgi import get_asgi_application\n\nfrom . import settings # noqa: F401"
            )
            file_contents = file_contents.replace(
                '"config.settings"',
                '"config.settings.dev"'
            )
            f.seek(0)
            f.write(file_contents)
            f.truncate()

    packages = [
        "argon2-cffi",
        "django-environ",
        "django-extensions",
        "django-debug-toolbar"
    ]

    {%- if cookiecutter.use_wagtail %}
    packages.append("wagtail"){% endif %}
    {%- if cookiecutter.use_vite_for_frontend %}
    packages.append("django-vite"){% endif %}
    {%- if cookiecutter.deployment_platform == "VPS" %}
    packages.extend(["django-redis", "hiredis"]){% endif %}

    print(HINT + "1. Ajouter les dépedances suivante à votre projet: " + TERMINATOR)
    for package in packages:
        print(HINT + f"- {package} " + TERMINATOR)
    print()
    {%- if cookiecutter.package_manager == "pipenv" %}
    print(HINT + f"=> pipenv install {' '.join(packages)}" + TERMINATOR){% elif cookiecutter.package_manager == "uv" %}
    print(HINT + f"=> uv add install {' '.join(packages)}" + TERMINATOR){% elif cookiecutter.package_manager == "poetry" %}
    print(HINT + f"=> poetry add {' '.join(packages)}" + TERMINATOR){% else %}
    print(HINT + f"=> pip install {' '.join(packages)}" + TERMINATOR){% endif %}
    print()
    print(HINT + "2. Copier _env.dev.exemple ou _env.prod.exemple à la racine de votre projet et renommez-le en .env" + TERMINATOR)
    print()
    print(HINT + '3. Ajouter path("__debug__/", include("debug_toolbar.urls")) à vos urls' + TERMINATOR)
    print()
    print(SUCCESS + "Vos fichiers de configuration sont prêts" + TERMINATOR)

    try:
        shutil.move(str(BASE_DIR / "settings"), str(CONFIG_DIR / "settings"))
    except PermissionError as e:
        shutil.rmtree(str(BASE_DIR / "settings))  # Supprime le dossier source après la copie

if __name__ == "__main__":
    main()
