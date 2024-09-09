from pathlib import Path
import sys


TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

def main():
    if not list(Path.cwd().parent.glob("manage.py")):
        print(WARNING + "Le répertoire courant ne semble pas être la racine d'un projet Django !" + TERMINATOR)
        print(WARNING + "- Pas de fichier manage.py à la racine" + TERMINATOR)
        sys.exit(1)

    if not list(Path.cwd().parent.rglob("wsgi.py")):
        print(WARNING + "Le répertoire courant ne semble pas être la racine d'un projet Django !" + TERMINATOR)
        print(WARNING + "- Aucun module wsgi.py n'a été trouvé" + TERMINATOR)
        sys.exit(1)


if __name__ == "__main__":
    main()
