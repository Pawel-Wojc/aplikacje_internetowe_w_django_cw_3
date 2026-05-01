from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('chat_home')
    return redirect('login')


from django.shortcuts import render

def render_error(request, status_code, message):
    return render(request, 'errors/error.html', {
        'status_code': status_code,
        'message': message,
    }, status=status_code)

def error_400(request, exception=None):
    return render_error(request, 400, 'Nieprawidłowe żądanie.')

def error_403(request, exception=None):
    return render_error(request, 403, 'Nie masz dostępu do tej strony.')

def error_404(request, exception):
    return render_error(request, 404, 'Taka strona nie istnieje.')

def error_500(request):
    return render_error(request, 500, 'Wewnętrzny błąd serwera.')