import jwt
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import CustomUserCreationForm
from user.models import User
from user.utils import Util


class SignUp(TemplateView):
    template_name = 'user/signup.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print(1222222222222222222)
            user_data = form.save()
            print(user_data)
            user = User.objects.get(username=user_data)
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('user:email-verify')
            absurl = 'http://' + current_site + relativeLink + '?token=' + str(token)
            email_body = 'Hi ' + user.username + ' Use link bellow to verify your email \n  ' + absurl
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
            Util.send_email(data)
            return redirect('user:login')
        context = {'form': form}
        return render(request, self.template_name, context)


class VerifyEmail(TemplateView):
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        print(token)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload['user_id'])
        try:
            if not user.is_active:
                user.is_active = True
                user.save()
                return render(request, 'user/activation_sent.html')
        except jwt.ExpiredSignatureError:
            return render(request, 'user/activation_sent.html')
        except jwt.exceptions.DecodeError:
            return render(request, 'user/account_invalid.html')


class UserUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'user/update.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        context = {'current_user': current_user}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST.get)
        print('##############')
        print(request.POST.get('username'))
        return HttpResponse('User is updated')
