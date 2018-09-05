Fun MOOC.
========================================================

Ce module permet une mise en forme facile avec la génération d'un fichier .css automatique pour les cours sur la plateforme FUN.

## Utilisation

### Structure d'un MOOC
Dans ce module, chaque MOOC est repéré par son nom (e.g. <i>mon_mooc</i>). A chaque MOOC est associé :
- un fichier <b>.css</b> : ce fichier défini la mise en forme qui apparaîtra sur la plateforme FUN.
- plusieurs dossiers :
    - <b>/css</b> : contient le fichier css appelé <i>xxx.css</i> où xxx est le nom du MOOC
    - <b>/exercices</b> : contient les fichiers .html des exercices (QCM)
    - <b>/evals</b> : contient les fichiers .html des évaluations
    - <b>/latex</b> : contient les fichiers .html traduits à partir d'un fichier .tex
    - <b>/other</b> : contient les autres fichiers .html
   
Dans chacun de ces dossiers, les fichiers html générés sont formatés pour être directement copiables sur la plateforme FUN tels quels.

##### ATTENTION : une fois le fichier css créé (instanciation du nouveau MOOC), il faudra impérativement l'uploader sur FUN sans quoi la mise en forme ne sera pas prise en compte. Chaque fois que le fichier est modifié, il faudra de nouveau l'uploader sur FUN.

### Le fichier .css

Le fichier css décrit la mise en forme du contenu qui apparaîtra sur la plateforme. Il défini plusieurs <i>environements</i> qui ont leur propre mise en forme. Par défaut sont créés les environnements :
- <b>default</b> : l'environnement par défaut. La couleur du fond est donnée par la variable `global_background_color`. Barres verticales à gauche pour les titres et ombre projetée.
- <b></b> :

### La classe `MOOC`

Une instance de `MOOC` est identifiée par son nom uniquement. Si le MOOC correcpondant n'existe pas, il sera créé.

#### Création et chargement d'un MOOC

A la première instanciation d'un objet `MOOC`, il vous sera demandé de renseigner le chemin (qui sera transformé en chemin global) du répertoire dans lequel vous voulez créer les MOOC. 
Chaque MOOC sera alors créé dans ce répertoire sous le nom `"mooc_XXX/"`.
```python
>>> from fun_mooc import*

>>> # créer un objet MOOC
>>> m = MOOC("mon_mooc")
...

```
A la création d'un objet `MOOC`, il vous sera demandé de donner les valeurs (en hexadécimal) de plusieurs environements. 
Pour chaque environement, cette couleur sera celle de la barre sur le côté et de son en-tête optionnel.

Pour changer ces couleurs, il suffit d'appeler la fonction `set_css_color(name, new_color)`. 
Pour créer un nouvel environnement, appeler la fonction `create_css_box`, par exemple:
```python
>>> # on charge un mooc déja existant
>>> m = MOOC("mon_mooc")
MOOC mon_mooc correctly loaded.
>>> # on crée un environnement nommé 'ma_boite'
>>> m.create_css_box("ma_boite", color="#efefef", header="Mon en-tête", shadow=True)
...
```






Ce code est sous licence WTFPL.
