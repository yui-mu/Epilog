from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import CustomUserCreationForm, SkincareRecordForm
from .models import SkincareRecord
from django.http import JsonResponse
from .forms import ProductForm
from .forms import ProductSearchForm
from .models import Product



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

def record_detail_view(request, pk):
    record = get_object_or_404(SkincareRecord, pk=pk, user=request.user)
    return render(request, 'record_detail.html', {'record': record})

def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

def product_search_view(request):
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get('name')
        brand = form.cleaned_data.get('brand')
        category = form.cleaned_data.get('category')
        ingredients = form.cleaned_data.get('ingredients')
        concerns = form.cleaned_data.get('concerns')

        if name:
            products = products.filter(name__icontains=name)
        if brand:
            products = products.filter(brand__icontains=brand)
        if category:
            products = products.filter(category__icontains=category)
        if ingredients:
                products = products.filter(ingredients__in=ingredients).distinct()
        if concerns:
                products = products.filter(concerns__in=concerns).distinct()
    return render(request, 'product_search.html', {
        'form': form,
        'products': products,
    })
