from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomLoginForm, CustomUserRegisterForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    authentication_form = CustomLoginForm
    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('home')


class RegisterView(CreateView):
    form_class = CustomUserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('chat')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('chat')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response