from django.contrib.auth import (
    logout,
)
from django.shortcuts import redirect


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def settings(request):
    user = request.user

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except Exception:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except Exception:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'accounts/settings.html', {
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Sua senha foi atualizada!')
            return redirect('accounts:settings')
        else:
            messages.error(request, 'Corriga os erros no formulário!')
    else:
        form = PasswordForm(request.user)
    return render(request, 'accounts/password.html', {'form': form})
