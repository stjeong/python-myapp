
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render


class RegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('bbs:index')


class SessionTestView(generic.View):
    template_name = 'session.html'

    def get(self, request):
        request.session['session_variable'] = 'test'
        return render(request, self.template_name)
