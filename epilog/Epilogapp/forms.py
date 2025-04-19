from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import SkincareRecord
from .models import Product
from .models import Ingredient, Concern

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
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'ingredients', 'concerns']
        widgets = {
            'ingredients': forms.CheckboxSelectMultiple,
            'concerns': forms.CheckboxSelectMultiple,
        }
        
class ProductSearchForm(forms.Form):
    name = forms.CharField(label='商品名', required=False)
    brand = forms.CharField(label='ブランド名', required=False)
    category = forms.CharField(label='カテゴリ', required=False)
    ingredients = forms.ModelMultipleChoiceField(
        label='配合成分',
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    concerns = forms.ModelMultipleChoiceField(
        label='対応する肌悩み',
        queryset=Concern.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )