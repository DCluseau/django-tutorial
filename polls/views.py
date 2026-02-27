from django.db.models import F
from django.db.models import Count, Sum, Max
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.views import generic
from .utils import minimax

from .models import Question, Choice

############## Constants ##############
NB_MAX_CHOIX = 5

############## Classes ##############
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]

class AllView(generic.ListView):
    template_name = "all.html"
    model = Question

    def get_queryset(self):
        """Return all published questions."""
        return Question.objects.order_by("id")

class DetailView(generic.DetailView):
    model = Question
    template_name = "detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class FrequencyView(generic.DetailView):
    model = Question
    template_name = "frequency.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "results.html"

############## Methods ##############

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def statistics(request):
    nbr_sondages = Question.objects.count()
    nbr_choix = Choice.objects.count()
    nbr_votes = \
        Choice.objects.aggregate(somme=Sum('votes'))['somme']
    moyenne_par_sondage = nbr_votes / nbr_sondages
    (question_la_moins_populaire, question_la_plus_populaire) = \
        minimax()
    id_derniere_question = \
        Question.objects.aggregate(max=Max('id'))['max']
    derniere_question = \
        Question.objects.get(pk=id_derniere_question)
    return render(request, 'statistics.html', {
    'nbr_sondages': nbr_sondages,
    'nbr_choix': nbr_choix,
    'nbr_votes': nbr_votes,
    'moyenne_par_sondage': moyenne_par_sondage,
    'question_la_plus_populaire': question_la_plus_populaire,
    'question_la_moins_populaire': question_la_moins_populaire,
    'derniere_question': derniere_question,
    })

def add(request):
    return render(request, 'add.html', {
    'liste_no_choix': range(NB_MAX_CHOIX)
    })

def confirm_add(request):
    # récupération du libellé de la question,
    # sans les éventuels espaces avant et après
    question_text = request.POST['question_text'].strip()
    if question_text:
        # ajout de la question si elle n'est pas vide
        question = Question(question_text=question_text,
        pub_date=timezone.now())
        question.save()
    # on traite à présent les champs de choix remplis
    # (on s'arrête au premier vide)
        for no_choix in range(NB_MAX_CHOIX):
            nom_champ = 'choix_{}'.format(no_choix)
            choice_text = request.POST[nom_champ].strip()
            if choice_text:
                choice = Choice(question=question,
                choice_text=choice_text)
                choice.save()
            else:
                break
        return render(request, 'confirm_add.html')
    else:
        # réaffichage du formulaire de saisie de la question
        # avec le message d'erreur
        return render(request, 'add.html', {
        'error_message': "You didn't enter a question text",
        })