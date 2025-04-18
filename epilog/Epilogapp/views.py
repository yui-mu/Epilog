from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import CustomUserCreationForm, SkincareRecordForm
from .models import SkincareRecord
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import SkincareRecord


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

def record_list_view(request):
    records = SkincareRecord.objects.filter(user=request.user).order_by('-record_date')
    return render(request, 'record_list.html', {'records': records})

def record_edit_view(request, pk):
    record = get_object_or_404(SkincareRecord, pk=pk, user=request.user)

    if request.method == 'POST':
        form = SkincareRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = SkincareRecordForm(instance=record)

    return render(request, 'record_form.html', {'form': form})

def record_delete_view(request, pk):
    record = get_object_or_404(SkincareRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        record.delete()
        return redirect('record_list')  # 削除後に一覧に戻る
    return render(request, 'record_confirm_delete.html', {'record': record})

def calendar_view(request):
    return render(request, 'record_calendar.html')

def calendar_events_view(request):
    records = SkincareRecord.objects.filter(user=request.user)
    events = []

    for record in records:
        events.append({
            "title": "記録あり",
            "start": str(record.record_date),
            "url": f"/record/{record.pk}/detail/"
        })

    return JsonResponse(events, safe=False)