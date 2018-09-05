Fun MOOC.
========================================================

Ce module permet une mise en forme facile avec la génération d'un fichier .css automatique pour les cours sur la plateforme FUN.

## Utilisation

La classe de base de ce module est la classe `MOOC`. 

Une instance de `MOOC` est identifiée par son nom uniquement. Si le MOOC correcpondant n'existe pas, il sera créé.

A la première instanciation d'un objet `MOOC`, il vous sera demandé de renseigner le chemin (qui sera transformé en chemin global) du répertoire dans lequel vous voulez créer les MOOC. 
Chaque MOOC sera alors créé dans ce répertoire sous le nom `"mooc_XXX/"`.
```python
from fun_mooc import*

# créer un objet MOOC
m = MOOC("mon_mooc")
...

```
A la création d'un objet `MOOC`, il vous sera demandé de donner les valeurs (en hexadécimal) de plusieurs environements. 
Pour chaque environement, cette couleur sera celle de la barre sur le côté et de son en-tête optionnel.

Pour changer ces couleurs, il suffit d'appeler la fonction `set_css_color(name, new_color)`. 
Pour créer un nouvel environnement, appeler la fonction `create_css_box`, par exemple:
```python
# on charge un mooc déja existant
m = MOOC("mon_mooc")
>>> MOOC mon_mooc correctly loaded.
# on crée un environnement nommé 'ma_boite'
m.create_css_box("ma_boite", color="#efefef", header="Mon en-tête", shadow=True)
...
```




Ce code est sous licence WTFPL.
