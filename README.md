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

Le fichier css décrit la mise en forme du contenu qui apparaîtra sur la plateforme. 
Il défini plusieurs <i>environements</i> qui ont leur propre mise en forme. 
Les environnements sont définis par 
- La couleur du fond : la même pour tout le MOOC et contrôlée par `global_background_color`
- La couleur de la barre latérale (à gauche) : si l'environnement s'appelle xxx, cette couleur s'apelle xxx_color
- La présence ou non d'une ombre
- Son en-tête : le texte qui apparaît en haut de l'environnement

A la création d'un MOOC, plusieurs environnements sont créés :
- <b>default</b> : l'environnement par défaut. Il ne contient pas d'en-tête ni de barre latérale. 
En revanche, chaque titre possède une barre dont la couleur est spécifiée par la variable `title_border_color`
- <b>latex</b> : l'environnement pour les pages laTex. Sans barre latérale non plus. Le résumé (spécifié en laTex par `\fbox{\parbox{\textwidth}{\textbf{Résumé} : `) possède une couleur propre donnée par la variable `latex_summary_background_color`
- <b>qcm</b> : l'environnement de QCM. L'en-tête est : <i>Exercice de compréhension</i>.
Il possède une barre latérale dont la couleur est spécifiée par la variable `qcm_color`
- <b>eval</b> : l'environnement des exercices d'évaluation. L'en-tête est : <i>Exercice d'évaluation</i>.
Il possède une barre latérale dont la couleur est spécifiée par la variable `eval_color`

Une fois le MOOC créé, il est possible de créer des environnements très simplement avec la mthéode `create_css_box`.

### La classe `MOOC`

Une instance de `MOOC` est identifiée par son nom uniquement. Si le MOOC correspondant n'existe pas, il sera créé.

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

Si le MOOC de ce nom existe déjà, il sera simplement chargé.

#### Editer le css d'un MOOC

Pour éditer l'apparence d'un MOOC, il faut éditer son fichier css. La classe `MOOC` possède plusieurs fonctions pour le faire simplement.
- Pour changer la couleur d'un environnement 'env' (c'est à dire la couleur de la barre latérale et de l'en-tête), il suffit d'appeler la fonction `set_css_color(env, new_color)`. 
- Pour créer un nouvel environnement, appeler la fonction `create_css_box`, par exemple:
```python
>>> # on charge un mooc déja existant
>>> m = MOOC("mon_mooc")
MOOC mon_mooc correctly loaded.
>>> # on crée un environnement nommé 'ma_boite'
>>> m.create_css_box(title="ma_boite", color="#efefef", header="Mon en-tête", lateral_bar=True, shadow=True)
...
```
- Pour mettre à jour une autre variable (e.g. la couleur du fond `global_background_color`), appeler la fonction `set_css_color(key, color)`

##### ATTENTION : chaque fois que le fichier css est modifié, il faudra de nouveau l'uploader sur FUN.

#### Formatter des fichiers pour FUN

Le coeur de la classe `MOOC` est de pouvoir formatter correctement des fichiers textes pour les rendre directement copiables sur FUN.
Il existe trois formatages différents :

- `generate_text()` : cette fonction lit le fichier en entrée et crée un fichier de sortie dans le répertoire <b>other/</b>.
Le texte ainsi généré peut être mis en forme selon l'environnement souhaité en spécifiant la variable `environment=...`
- `generate_latex_page()` : met en page un fichier .tex de manière à ce qu'il apparaisse correctemeent sur FUN.
    * remarque 1 : cette fonction nécéssite [pandoc](https://pandoc.org/) !
    * remarque 2 : cette fonction repère les 'résumés' laTex quand ils sont formatés de la manière suivante :
    ```latex
    \fbox{\parbox{\textwidth}{\textbf{Résumé} : ceci est mon résumé }}
    ```
- `generate_exercice()` : met en page un fichier (texte) de façon à générer des exerices (QCM ou évaluation). Pour être correctement interprété, ce fichier doit être formaté comme selon cet exemple :
```text
é contenu du fichier d'input, disons 'input.txt'
# un qcm
QCM: Quelle est la couleur du cheval blanc d'Henry IV ?
- Bleu
-A Blanc
- Euh ...

# une liste déroulante. La réponse est 'lol'
CHOICE: Il fait beau à Paris :
((c'est vrai, ça dépend, *lol, c'est mon dernier mot))

# insertion d'une image. le fichier 'test.png' doit être uploadé sur FUN.
IMAGE: test.png

# Une boîte d'entrée (de strings). Cette fois ci, on spécifie toutes les réponses possibles
INPUT: Quel est le premier entier impair supérieur à 5 ?
((5, 7)) # on va dire qu'on accepte 5 vu que 'strictement' n'est pas spécifié !

# et puis du texte quelconque
Voici une belle phrase qui va apparaître telle quelle. Sauf que $\alpha=3x^2$ sera formaté en mathjax, ainsi que 
\begin{equation}
    R_{\mu\nu} -\frac{1}{2}g_{\mu\nu}R \propto T_{\mu\nu}
\end{equation}
```

Les différents exercices reconnus sont donc :
- `QCM:` : un exercice à choix multiples. Le ou les bonnes réponses sont repérées par le `-A`
- `CHOICE:` : liste déroulante. Le bon choix est répéré par l'étoile `*`
- `INPUT:` : saisie d'une réponse (chaîne de caractère). On spécifie le ou les bonnes réponses.
- Plus les `IMAGE:` et le texte normal qui est juste formaté pour afficher correctement le code laTex. 

Pour formatter un tel fichier, il suffit alors d'appeler 
```python
>>> # on charge un mooc déja existant (ou on le crée)
>>> m = MOOC("mon_mooc")
MOOC mon_mooc correctly loaded.
>>> # on formatte un fichier d'entrée. Disons qu'il s'apelle '../input.txt'
>>> m.generate_exerice(source_file='../input.txt', output_name='fichier_sortie', is_evaluation=True)

```
Ce code est sous licence WTFPL.
