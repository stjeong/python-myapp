# Create your views here.

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'bbs/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'bbs/index.html', context)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'bbs/detail.html'


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("{0} Question does not exist".format(question_id))
    return render(request, 'bbs/detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'bbs/detail.html', {'question': question})

    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('bbs:results', args=(question_id,)))


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'bbs/results.html'


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'bbs/results.html', {'question': question})


def parent(request):
    return render(request, 'bbs/base.html')


def child(request):
    return render(request, 'bbs/child.html')

