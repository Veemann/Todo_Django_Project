from django import forms  
from .models import Task 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

class TaskForm (forms.ModelForm):
    due_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    class Meta:
        model = Task
        fields = ('title', 'done', 'due_time')
        exclude = ('user',)
        
class RegisterForm (UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
     
     