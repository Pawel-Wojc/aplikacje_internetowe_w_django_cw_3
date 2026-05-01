from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserSettingsForm, CustomUserPasswordChangeForm
from django.contrib import messages
from .forms import CustomLoginForm, CustomUserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    authentication_form = CustomLoginForm
    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('chat_home')


class RegisterView(CreateView):
    form_class = CustomUserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('chat_home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('chat_home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
    

@login_required
def profile_view(request):
    if request.method == 'POST':
        if 'save_profile' in request.POST:
            profile_form = UserSettingsForm(
                request.POST,
                request.FILES,
                instance=request.user
            )
            password_form = CustomUserPasswordChangeForm(request.user)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profil został zaktualizowany.')
                return redirect('profile')

        elif 'change_password' in request.POST:
            profile_form = UserSettingsForm(instance=request.user)
            password_form = CustomUserPasswordChangeForm(request.user, request.POST)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Hasło zostało zmienione.')
                return redirect('profile')

        else:
            profile_form = UserSettingsForm(instance=request.user)
            password_form = CustomUserPasswordChangeForm(request.user)

    else:
        profile_form = UserSettingsForm(instance=request.user)
        password_form = CustomUserPasswordChangeForm(request.user)
    print(profile_form.errors)
    return render(request, 'accounts/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })