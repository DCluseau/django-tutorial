# Django
## Compte-rendu exercice 2.2.2.1

J’ai ajouté le code suivant à admin.py :
```
admin.site.register(Choice)
```

L’interface est bien apparue et j’ai pu enregistrer de nouvelles questions et réponses :
    • What is your name ?
        ◦ Sir Lancelot of Camelot
        ◦ Sir Robin of Camelot
        ◦ It is 'Arthur', King of the Britons
    • What is your quest?
        ◦ To seek the Holy Grail
        ◦ I seek the Grail
        ◦ Eating pizza
    • What is your favourite colour?
        ◦ Blue
        ◦ Blue. No, yel…
        ◦ Octarine
    • What is the capital of Assyria?
        ◦ I don't know that!
        ◦ Assur
        ◦ R'Lyeh
    • What is the air-speed velocity of an unladen swallow? 
        ◦ What do you mean? An African or European swallow?
        ◦ Huh? I... I don't know that.
        ◦ 299 792 458 m/s
Les attributs, les filtres et la recherche n’apparaissent pas car l’interface n’a pas été modifiée dans admin.py.
	```
  @admin.register(Question)
		class QuestionAdmin(Question):
		    pass
  ```
Le code complet jusqu’à présent dans admin.py est le suivant :
```
from django.contrib import admin

from .models import Question
from .models import Choice

class QuestionAdmin(admin.ModelAdmin):
	list_display = ["question_text", "pub_date"]
	list_filter = ["question_text", "pub_date"]
	ordering = ["-pub_date", "question_text"]
	search_fields = ["question_text", "pub_date"]
	pass
admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
	list_display = ["question", "choice_text", "votes"]
	list_filter = ["question", "choice_text", "votes"]
	ordering = ["question", "choice_text", "votes"]
	search_fields = ["choice_text", "votes", "foreign_key__related_fieldname"]
	pass
admin.site.register(Choice, ChoiceAdmin)
```
J’ai ajouté un utilisateur sans lui mettre de statut. Impossible de se connecter avec ses identifiants.
Cela arrive car il ne fait pas partie d’un groupe qui peut accéder à l’interface Admin.
Si on lui met le statut « Équipe », il peut se connecter mais ne peut rien modifier. Par contre, si on lui met le statut « Super-utilisateur », il peut modifier des éléments, comme l’utilisateur admin.
Pour désactiver l’utilisateur, il suffit de décocher la case « Actif » dans ses paramètres.
