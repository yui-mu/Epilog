from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from .models import CustomUser
from .models import SkincareRecord
from .models import Product, Concern, SkinType


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'nickname', 'email', 'password1', 'password2')

SKIN_CONCERN_CHOICES = [
    ('dry', '乾燥'),
    ('dull', 'くすみ'),
    ('wrinkle', 'シワたるみ'),
    ('spot', 'シミ'),
    ('pore', '毛穴'),
    ('acne', '赤み・ニキビ'),
]

SKIN_RATING_CHOICES = [
    ('very_good', 'とても良い'),
    ('good', '良い'),
    ('normal', '普通'),
    ('slightly_bad', 'やや悪い'),
    ('bad', '悪い'),
]

class SkincareRecordForm(forms.ModelForm):
    concerns = forms.MultipleChoiceField(
        choices=SKIN_CONCERN_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='肌悩み'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['record_date'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

    class Meta:
        model = SkincareRecord
        fields = [
            'record_date', 'photo', 'skin_condition',
            'morning_items', 'night_items',
            'skin_rating', 'concerns'
        ]
        widgets = {
            'skin_rating': forms.RadioSelect,  # ← ここでラジオボタンにする
        }



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'image', 'ingredients', 'concerns']
        widgets = {
            'ingredients': forms.CheckboxSelectMultiple,
            'concerns': forms.CheckboxSelectMultiple,
        }
        
class ProductSearchForm(forms.Form):
    keyword = forms.CharField(
        label='キーワード（商品名・ブランド名・成分名）',
        required=False
    )
    category = forms.ChoiceField(
        label='カテゴリ',
        choices=[('', '---')] + Product.CATEGORY_CHOICES,
        required=False
    )
    concern = forms.ModelChoiceField(
        label='悩み・効果',
        queryset=Concern.objects.all(),
        empty_label='---',
        required=False
    )
    skin_type = forms.ModelChoiceField(
        label='肌質',
        queryset=SkinType.objects.all(),
        empty_label='---',
        required=False
    )
    feature = forms.CharField(
        label='成分の特徴（例：保湿、低刺激など）',
        required=False
    )
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nickname', 'age', 'concerns', 'profile_photo']
        widgets = {
            'concerns': forms.CheckboxSelectMultiple,
        }
        
class UserEditForm(UserChangeForm):
    password = None  # パスワードは表示しない

    class Meta:
        model = CustomUser
        fields = ['username', 'email']
        
User = get_user_model()

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'age', 'concerns']
        widgets = {
            'concerns': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'nickname': 'ニックネーム',
            'age': '年齢',
            'concerns': '肌の悩み（2個くらい）',
        }
        
User = get_user_model()

class EditAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'ユーザー名',
            'email': 'メールアドレス',
        }
        
class EmailLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'you@example.com'
    }))
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'パスワードを入力'
    }))