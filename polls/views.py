from django.db.models import F
from django.db.models.aggregates import Count, Sum
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.views import generic

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
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return all published questions."""
        return Question.objects.order_by("question_text")

class DetailView(generic.DetailView):
    model = Question
    template_name = "detail.html"

class FrequencyView(generic.DetailView):
    model = Question
    template_name = "frequency.html"

class StatisticsView(generic.ListView):
    template_name = "statistics.html"
    context_object_name = "question_list"

    def get_queryset(self):
        """Return all published questions."""
        return Question.objects.order_by("question_text")

    @staticmethod
    def get_total_nb_of_choices():
        model = Question
        count = 0
        return count

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