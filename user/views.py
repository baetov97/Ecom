from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.forms import UserCreationForm

from user.models import User


class SignUp(TemplateView):
    template_name = 'user/signup.html'

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')


class UserUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'user/update.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        context = {'current_user': current_user}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print('##############')
        print(request.POST.get('username'))
        return HttpResponse('User is updated')
