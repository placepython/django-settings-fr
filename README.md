# Générateur de settings Django avec commentaires en français

Ce template Cookiecutter a pour objectif de générer un répertoire de settings séparés Django pour
les environnements de développement et de production.

Chaque variable de configuration est commentée en français pour permettre à tout débutant
francophone de démarrer rapidement avec leurs premiers déploiement.

## Génération du répertoire de settings:

La procédure suivante vous permettra de générer des settings personnalisés séparés pour le dev et
la production. Vous aurez besoin de l'outil Cookiecutter que vous pouvez installer au préalable
à l'aide de la commande `pip install cookiecutter`. Vous pouvez également utiliser cookiecutter
sans installation si vous l'utilisez [uv](https://docs.astral.sh/uv/) en préfixant les commandes par uvx.

1. Ouvrir un terminal à la racine de votre projet Django.
2. Générer un répertoire de settings à l'aide de la commande `cookiecutter gh:placepython/django-settings-fr`
3. Répondez aux questions posées
4. Suivez les instructions affichées dans le terminal à la fin de l'installation
