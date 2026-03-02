from django.db.models import F
from django.db.models import Sum, Max
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .utils import minimax

from .forms import VoteForm, QuestionAddForm

from .models import Question, Choice

############## Constants ##############
NB_MAX_CHOIX = 5

############## Classes ##############
class IndexView(generic.ListView):
    template_name = "index.html"
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

# fusion et modification de la classe DetailView et # de la méthode vote en la seule méthode vote
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices_form = [(choice.id, choice.choice_text) for choice in question.choice_set.all()]
    if request.method == 'POST':
        form = VoteForm(question.question_text,
        choices_form, request.POST)
        if form.is_valid():
            selected_choice = \
            question.choice_set.get(pk=form.cleaned_data['choice'])
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    else:
        form = VoteForm(question.question_text, choices_form)
    return render(request, 'detail.html',
        {'form': form, 'question': question})

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

# fusion et modification des méthodes add et confirm_add # en la seule méthode add
def add(request):
    if request.method == 'POST':
        form = QuestionAddForm(request.POST)
        if form.is_valid():
            question = \
            Question(question_text=\
            form.cleaned_data['question_text'],
            pub_date=timezone.now())
            question.save()
        # on traite à présent les champs de choix remplis
        # (on s'arrête au premier vide)
            for no_choix in range(NB_MAX_CHOIX):
                nom_champ = 'choice_{}'.format(no_choix)
                choice_text = form.cleaned_data[nom_champ].strip()
                if choice_text:
                    choice = Choice(question=question, choice_text=choice_text)
                    choice.save()
                else:
                    break
            return render(request, 'polls/confirm_add.html')
    else:
        form = QuestionAddForm()
    return render(request, 'polls/add.html', {'form': form})
