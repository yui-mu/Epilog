from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import SkincareRecord

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'nickname', 'email', 'password1', 'password2')
class SkincareRecordForm(forms.ModelForm):
    class Meta:
        model = SkincareRecord
        fields = [
            'record_date',
            'skin_rating',
            'skin_condition',
            'photo',
            'morning_items',     
            'night_items',       
            'concerns',          
            'ingredients',       
        ]

        widgets = {
            'record_date': forms.DateInput(attrs={'type': 'date'}),
            'skin_rating': forms.Select(),
            'skin_condition': forms.Textarea(attrs={'rows': 3}),
            'morning_items': forms.Textarea(attrs={'rows': 2}),
            'night_items': forms.Textarea(attrs={'rows': 2}),
            'concerns': forms.Textarea(attrs={'rows': 2}),
            'ingredients': forms.Textarea(attrs={'rows': 2}),
        }