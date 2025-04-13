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
        fields = ['record_date', 'skin_rating', 'skin_condition', 'photo']

        widgets = {
            'record_date': forms.DateInput(attrs={'type': 'date'}),
            'skin_rating': forms.Select(),
            'skin_condition': forms.Textarea(attrs={'rows': 4}),
        }