from django.db.models import F
from django.db.models import Count, Sum, Max
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.views import generic

from .utils import minimax

from .models import Question, Choice

def nb(list_questions):
    nb_choices = 0
    for question in list_questions:
        nb_choices += question.aggregate(Count('choices'))
    return nb_choices

class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

class AllView(generic.ListView):
    template_name = "all.html"
    model = Question

    def get_queryset(self):
        """Return all published questions."""
        return Question.objects.order_by("id")

class DetailView(generic.DetailView):
    model = Question
    template_name = "detail.html"

class FrequencyView(generic.DetailView):
    model = Question
    template_name = "frequency.html"

# class StatisticsView(generic.ListView):
#     template_name = "statistics.html"
#     context_object_name = "question_list"
#
#     def get_queryset(self):
#         """Return all published questions."""
#         return Question.objects.order_by("question_text")
#
#     @staticmethod
#     def get_total_nb_of_choices():
#         model = Question
#         count = 0
#         return count

class ResultsView(generic.DetailView):
    model = Question
    template_name = "results.html"

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