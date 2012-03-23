import string
from random import Random

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail

from shortcuts import request_to_response

from accounts import models

#===============================================================================
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20, 
        required=True
    )
    password = forms.CharField(
        max_length=20, 
        widget=forms.PasswordInput, 
        required=True
    )
    
    #---------------------------------------------------------------------------
    def __init__(self, request, *args, **kws):
        super(LoginForm, self).__init__(*args, **kws)
        self.request = request
    
    #---------------------------------------------------------------------------
    def clean(self):
        super(LoginForm, self).clean()
        
        data = self.cleaned_data
        user = authenticate(
            username=data.get('username', ''), 
            password=data.get('password', '')
        )
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return True
            else:
                raise forms.ValidationError(message=u'Account is disabled.')
        else:
            raise forms.ValidationError(message=u'Invalid username/password.')
        
        return False

#===============================================================================
class AccountCreateForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    number = forms.CharField(
        max_length=10, 
        required=False, 
        help_text='Your CoBuyer account number'
    )
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput,
        required=True
    )
    password_confirm = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput,
        required=True
    )
    email = forms.EmailField()
    
    #---------------------------------------------------------------------------
    def __init__(self, request, *args, **kws):
        super(AccountCreateForm, self).__init__(*args, **kws)
        self.request = request
    
    #---------------------------------------------------------------------------
    def clean_password_confirm(self):
        data = self.cleaned_data
        
        if not data['password_confirm']:
            raise forms.ValidationError(message=u'Confirm Password value is required.')
        
        if data['password_confirm'] != data['password']:
            raise forms.ValidationError(message=u'Confirm Password does not match Password.')
        
        return data['password_confirm']
    
    #---------------------------------------------------------------------------
    def clean_username(self):
        data = self.cleaned_data
        
        if not data['username']:
            raise forms.ValidationError(message=u'Username is required.')
        
        if User.objects.filter(username=data['username']):
            raise forms.ValidationError(message=u'Username is already in use.')
        
        return data['username']
    
    #---------------------------------------------------------------------------
    def save(self):
        data = self.cleaned_data
        
        user = User.objects.create_user(
            data['username'],
            data['email'],
            data['password']
        )
        
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()
        
        profile = models.UserProfile.objects.create(
            user=user,
            number=data['number'],
        )
        
        subject = 'Confirm New Account'
        data = dict(
            user=user,
            data=data,
        )
        message = request_to_response(self.request, 'accounts/email/new_account.txt', data)
        send_mail(subject, message, settings.EMAIL_FROM, [user.email], fail_silently=True)
        
        return user

#===============================================================================
class AccountForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    number = forms.CharField(
        max_length=10, 
        required=False, 
        help_text='Your CoBuyer account number'
    )
    email = forms.EmailField()
    
    #---------------------------------------------------------------------------
    def __init__(self, request, *args, **kws):
        super(AccountForm, self).__init__(*args, **kws)
        self.request = request
        self.user = User.objects.get(username=self.request.user.username)
        self.profile = models.UserProfile.objects.get(user=self.user)
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name
        self.fields['number'].initial = self.profile.number
        self.fields['email'].initial = self.user.email
    
    #---------------------------------------------------------------------------
    def save(self):
        data = self.cleaned_data
        
        self.user.first_name = data['first_name']
        self.user.last_name = data['last_name']
        self.user.save()
        
        self.profile.number=data['number']
        self.profile.save()
        
        return self.user

#===============================================================================
class PasswordForm(forms.Form):
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput,
        required=True
    )
    password_confirm = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput,
        required=True
    )
    
    #---------------------------------------------------------------------------
    def __init__(self, request, *args, **kws):
        super(PasswordForm, self).__init__(*args, **kws)
        self.request = request
    
    #---------------------------------------------------------------------------
    def clean_password_confirm(self):
        data = self.cleaned_data
        
        if not data['password_confirm']:
            raise forms.ValidationError(message=u'Confirm Password value is required.')
        
        if data['password_confirm'] != data['password']:
            raise forms.ValidationError(message=u'Confirm Password does not match Password.')
        
        return data['password_confirm']
    
    #---------------------------------------------------------------------------
    def save(self):
        data = self.cleaned_data
        
        user = self.request.user
        user.set_password(data['password'])
        user.save()
        
        return user

#===============================================================================
class ResetPasswordForm(forms.Form):
    email = forms.EmailField()
    
    #---------------------------------------------------------------------------
    def __init__(self, request, *args, **kws):
        super(ResetPasswordForm, self).__init__(*args, **kws)
        self.request = request
    
    #---------------------------------------------------------------------------
    def clean_email(self):
        data = self.cleaned_data
        
        if not data['email']:
            raise forms.ValidationError(message=u'An email is required.')
        
        if not User.objects.filter(email=data['email']):
            raise forms.ValidationError(message=u'No email address not found.')
        
        return data['email']
        
    #---------------------------------------------------------------------------
    def save(self):
        data = self.cleaned_data
        
        user = User.objects.get(email=data['email'])
        password = ''.join(Random().sample(string.letters+string.digits, 6))
        user.set_password(password)
        user.save()
        
        subject = 'Password Updated'
        data = dict(
            user=user,
            data=data,
            password=password,
        )
        message = request_to_response(self.request, 'accounts/email/new_password.txt', data)
        send_mail(subject, message, settings.EMAIL_FROM, [user.email], fail_silently=False)
        
        return user