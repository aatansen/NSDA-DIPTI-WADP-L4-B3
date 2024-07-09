from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from .models import *
from django.forms.widgets import PasswordInput

class Custom_user_form(UserCreationForm):
    class Meta:
        model=Custom_user_model
        fields=['username','Display_name','email','User_Type']
        help_texts={
            'username':None
        }

class Auth_form(AuthenticationForm):
    class Meta:
        model=Custom_user_model
        fields=['username','password']
        
class Job_form(forms.ModelForm):
    class Meta:
        model=Job_model
        fields='__all__'
        exclude=['created_by']


class Job_apply_form(forms.ModelForm):
    class Meta:
        model=Job_apply_model
        fields='__all__'
        exclude=['Applicant','Applied_Job','Status']

class Edit_basic_form(forms.ModelForm):
    class Meta:
        model=Custom_user_model
        fields=['Display_name']

class Edit_seeker_form(forms.ModelForm):
    class Meta:
        model=Seeker_model
        fields='__all__'
        exclude=['seeker_user']

class Edit_recruiter_form(forms.ModelForm):
    class Meta:
        model=Recruiter_model
        fields='__all__'
        exclude=['recruiter_user']


