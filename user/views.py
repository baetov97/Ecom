import jwt
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
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
            user_data = form.save()
            user = User.objects.get(username=user_data)
            user.is_active = False
            user.save()
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('user:email-verify')
            absurl = 'http://' + current_site + relativeLink + '?token=' + str(token)
            email_body = 'Hi ' + user.username + ' Use link bellow to verify your email \n  ' + absurl
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
            Util.send_email(data)
            return redirect('user:activation_sent')
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
                login(request, user)
                return render(request, 'user/completed-success.html')
        except jwt.ExpiredSignatureError:
            return render(request, 'user/account_invalid.html')
        except jwt.exceptions.DecodeError:
            return render(request, 'user/account_invalid.html')
        return render(request, 'user/account_invalid.html')


def activation_sent(request):
    return render(request, 'user/activation_sent.html')


class UserUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'user/update.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        context = {'current_user': current_user}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        user = User.objects.get(email=request.user.email)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.save()
        return JsonResponse({'user': 'Successfully updated'}, status=200)
