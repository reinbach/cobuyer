from django import http
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from cart import models as cart
from shortcuts import request_to_response

from accounts import models, forms

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request, data=request.POST)
        if form.is_valid():
            return http.HttpResponseRedirect(reverse('account_home'))
    else:
        form = forms.LoginForm(request)
    data = dict(
        form=form,
    )
    return request_to_response(request, 'accounts/login.html', data)

#-------------------------------------------------------------------------------
def logout_user(request):
    logout(request)
    form = forms.LoginForm(request)
    data = dict(
        messages=[u'You have been logged out.',],
        form=form,
    )
    return request_to_response(request, 'accounts/login.html', data)

#-------------------------------------------------------------------------------
def create(request):
    if request.method == 'POST':
        form = forms.AccountCreateForm(request, data=request.POST)
        if form.is_valid():
            user = form.save()
            form = forms.LoginForm(request)
            data = dict(
                messages=['A new account has been created.',],
                form=form
            )
            return request_to_response(request, 'accounts/login.html', data)
    else:
        form = forms.AccountCreateForm(request)
    data = dict(
        form=form,
    )
    return request_to_response(request, 'accounts/create.html', data)

#-------------------------------------------------------------------------------
def reset_password(request):
    if request.method == 'POST':
        form = forms.ResetPasswordForm(request, data=request.POST)
        if form.is_valid():
            user = form.save()
            form = forms.LoginForm(request)
            data = dict(
                messages=[u'A new Password has been sent to %s.' % user.email],
                form=form
            )
            return request_to_response(request, 'accounts/login.html', data)
    else:
        form = forms.ResetPasswordForm(request)
    data = dict(
        form=form
    )
    return request_to_response(request, 'accounts/reset_password.html', data)
    
#-------------------------------------------------------------------------------
@login_required(redirect_field_name='login')
def home(request):
    profile = get_object_or_404(models.UserProfile, user=request.user)
    past_orders = cart.Cart.objects.filter(user=request.user, completed=True)
    data = dict(
        profile=profile,
        past_orders=past_orders,
    )
    return request_to_response(request, 'accounts/index.html', data)

#-------------------------------------------------------------------------------
@login_required(redirect_field_name='login')
def update(request):
    if request.method == 'POST':
        form = forms.AccountForm(request, data=request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message=u'Account profile has been updated.')
            return http.HttpResponseRedirect(reverse('account_home'))
    else:
        form = forms.AccountForm(request)
    data = dict(
        form=form
    )
    return request_to_response(request, 'accounts/update.html', data)

#-------------------------------------------------------------------------------
@login_required(redirect_field_name='login')
def password(request):
    if request.method == 'POST':
        form = forms.PasswordForm(request, data=request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message=u'Account password has been updated.')
            return http.HttpResponseRedirect(reverse('account_home'))
    else:
        form = forms.PasswordForm(request)
    data = dict(
        form=form
    )
    return request_to_response(request, 'accounts/password.html', data)
