from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SkincareRecordForm


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 登録後にログインページへ
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'home.html')

def top_view(request):
    return render(request, 'top.html')

def record_create_view(request):
    if request.method == 'POST':
        form = SkincareRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user  # ログインユーザーを紐付け
            record.save()
            return redirect('home')  # 登録後にホームへ戻る
    else:
        form = SkincareRecordForm()
    return render(request, 'record_form.html', {'form': form})