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
from .models import Favorite
from .models import Message
from django.utils import timezone
from .models import CustomUser





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

@login_required
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

@login_required
def record_list_view(request):
    records = SkincareRecord.objects.filter(user=request.user).order_by('-record_date')
    return render(request, 'record_list.html', {'records': records})

@login_required
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

@login_required
def record_delete_view(request, pk):
    record = get_object_or_404(SkincareRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        record.delete()
        return redirect('record_list')  # 削除後に一覧に戻る
    return render(request, 'record_confirm_delete.html', {'record': record})

@login_required
def calendar_view(request):
    return render(request, 'record_calendar.html')

@login_required
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

@login_required
def record_detail_view(request, pk):
    record = get_object_or_404(SkincareRecord, pk=pk, user=request.user)
    return render(request, 'record_detail.html', {'record': record})

@login_required
def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

@login_required
def product_search_view(request):
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.none()  # 初期は空にする

    if form.is_valid() and request.GET:  # ← GETデータがあるときだけ実行！
        name = form.cleaned_data.get('name')
        brand = form.cleaned_data.get('brand')
        category = form.cleaned_data.get('category')
        ingredients = form.cleaned_data.get('ingredients')
        concerns = form.cleaned_data.get('concerns')

        products = Product.objects.all()

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

@login_required
def add_favorite_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if created:
        message = "お気に入りに追加しました！"
    else:
        message = "すでにお気に入りに登録されています。"

    # ホームや検索結果ページにリダイレクト
    return redirect('product_search')

@login_required
def favorite_list_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'favorite_list.html', {'favorites': favorites})

@login_required
def remove_favorite_view(request, product_id):
    favorite = Favorite.objects.filter(user=request.user, product_id=product_id).first()
    if favorite:
        favorite.delete()
    return redirect('favorite_list')

@login_required
def chat_view(request):
    user = request.user
    advisor = None

    if not user.is_advisor:
        advisor = CustomUser.objects.filter(is_advisor=True).first()

    if user.is_advisor:
        messages = Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
    else:
        messages = Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
        if advisor:
            messages |= Message.objects.filter(receiver=advisor)

    messages = messages.order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            if user.is_advisor:
                receiver_id = request.POST.get('receiver')
                try:
                    receiver = CustomUser.objects.get(id=receiver_id)
                    Message.objects.create(sender=user, receiver=receiver, content=content)
                except CustomUser.DoesNotExist:
                    pass  # 無効なユーザーIDだった場合
            else:
                if advisor:
                    Message.objects.create(sender=user, receiver=advisor, content=content)
        return redirect('chat')

    # アドバイザー用：全ユーザー一覧を渡す
    user_list = CustomUser.objects.filter(is_advisor=False) if user.is_advisor else None

    return render(request, 'chat.html', {
        'messages': messages,
        'user_list': user_list,
    })











