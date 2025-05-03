from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from collections import Counter
from .forms import (
    CustomUserCreationForm, 
    SkincareRecordForm, 
    ProductForm, 
    ProductSearchForm,
    ProfileForm, 
    UserEditForm,
    EditAccountForm,
    EmailLoginForm,
    )
from .models import (
    SkincareRecord, Product, 
    Favorite, Message, CustomUser, SKIN_CONCERN_CHOICES,ChatSession, Message)
import ast


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            # バリデーションに失敗したときも、formをそのまま渡して再表示
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def email_login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # ログイン後に表示したいページ
            else:
                form.add_error(None, 'メールアドレスまたはパスワードが正しくありません。')
    else:
        form = EmailLoginForm()
    return render(request, 'registration/login.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        # メールアドレスをセッションに保存
        self.request.session['reset_email'] = form.cleaned_data['email']
        return super().form_valid(form)

class CustomPasswordResetDoneView(TemplateView):
    template_name = 'registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session.get('reset_email', 'ご登録のメールアドレス')
        return context

@login_required
def home_view(request):
    if request.user.is_advisor:
        return render(request, 'advisor/home.html')
    else:
        return render(request, 'home.html')

def top_view(request):
    return render(request, 'top.html')

@login_required
def record_create_view(request):
    initial_date = request.GET.get('date')
    
    morning_list = []
    night_list = []

    # ユーザーの過去記録から朝・夜アイテムのテキストを集める
    records = SkincareRecord.objects.filter(user=request.user)
    used_names = []

    for record in records:
        if record.morning_items:
            used_names.extend(record.morning_items.split(','))
        if record.night_items:
            used_names.extend(record.night_items.split(','))

    # よく使われた商品名を集計
    cleaned = [name.strip() for name in used_names if name.strip()]
    most_common = [name for name, count in Counter(cleaned).most_common(10)]

    # 一致する商品オブジェクトを取得
    products = Product.objects.filter(name__in=most_common)

    if not products.exists():  # fallback
        products = Product.objects.all()

    # フォーム処理
    if request.method == 'POST':
        form = SkincareRecordForm(request.POST, request.FILES)
        print("POSTで送られたデータ:", request.POST)
        
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return render(request, 'record_complete.html')
        else:
            print("フォームのエラー:", form.errors)
    else:
        date_str = request.GET.get('date')
        try:
            initial_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        except (TypeError, ValueError):
            initial_date = timezone.now().date()
        
        form = SkincareRecordForm(initial={'record_date': initial_date})

        morning_text = request.POST.get('morning_items', '')
        night_text = request.POST.get('night_items', '')

        morning_list = [s.strip() for s in morning_text.split(',') if s.strip()] if morning_text else []
        night_list = [s.strip() for s in night_text.split(',') if s.strip()] if night_text else []
    return render(request, 'record_form.html', {
    'form': form,
    'products': products,
    'morning_list': morning_list,
    'night_list': night_list,
})

@login_required
def record_list_view(request):
    sort = request.GET.get('sort', 'desc')
    order = '-record_date' if sort == 'desc' else 'record_date'
    records = SkincareRecord.objects.filter(user=request.user).order_by(order)
    return render(request, 'record_list.html', {'records': records})

@login_required
def record_edit_view(request, pk):
    record = get_object_or_404(SkincareRecord, pk=pk, user=request.user)

    if request.method == 'POST':
        form = SkincareRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            record = form.save(commit=False)

            record.morning_items = request.POST.get('morning_items', '')
            record.night_items = request.POST.get('night_items', '')

            record.save()
            return redirect('record_detail', pk=record.pk)
    else:
        form = SkincareRecordForm(instance=record, initial={
        'morning_items': record.morning_items,
        'night_items': record.night_items,
        })

    return render(request, 'record_form.html', {
        'form': form,
    })


                   

@login_required
def calendar_view(request):
    return render(request, 'record_calendar.html')

@login_required
def calendar_events_view(request):
    records = SkincareRecord.objects.filter(user=request.user)
    events = []

    for record in records:
        events.append({
    "title": "記録あり",  # ← 文字をちゃんと表示
    "start": str(record.record_date),
    "url": f"/record/{record.pk}/detail/",
    "className": "recorded-day-fullclick"
})

    return JsonResponse(events, safe=False)
   
@login_required
def record_detail_view(request, pk):
    record = get_object_or_404(SkincareRecord, pk=pk, user=request.user)
    
    print("DEBUG - morning_items:", record.morning_items)
    print("DEBUG - night_items:", record.night_items)


    # カテゴリと商品名に分割する関数（辞書形式で返す）
    def parse_items(item_string):
        result = []
        for item in item_string.split(','):
            item = item.strip()
            if not item:
                continue
            parts = item.split(':')
            category = parts[0] if len(parts) > 0 else "未分類"
            name = parts[1] if len(parts) > 1 else ""
            ingredient = parts[2] if len(parts) > 2 else ""
            result.append({
                'category': category.strip(),
                'name': name.strip(),
                'ingredient': ingredient.strip(),
            })
        return result


    morning_list = parse_items(record.morning_items or "")
    night_list = parse_items(record.night_items or "")

    
    CONCERN_DICT = dict(SKIN_CONCERN_CHOICES)
    concerns_list = []
    
    if record.concerns:
        try:
            parsed = ast.literal_eval(record.concerns)
            if isinstance(parsed, list):
                concerns_list = [CONCERN_DICT.get(item.strip(), item.strip()) for item in parsed if item.strip()]
            elif isinstance(parsed, str) and parsed.strip():
                concerns_list = [CONCERN_DICT.get(parsed.strip(), parsed.strip())]
        except:
            if record.concerns.strip():
                concerns_list = [CONCERN_DICT.get(record.concerns.strip(), record.concerns.strip())]

    return render(request, 'record_detail.html', {
        'record': record,
        'morning_list': morning_list,
        'night_list': night_list,
        'concerns_list': concerns_list,
    })

@login_required
def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

@login_required
def product_search_view(request):
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.all()

    if form.is_valid() and request.GET:
        keyword = form.cleaned_data.get('keyword')
        category = form.cleaned_data.get('category')
        concern = form.cleaned_data.get('concern')
        skin_type = form.cleaned_data.get('skin_type')
        feature = form.cleaned_data.get('feature')

        if keyword:
            products = products.filter(
                Q(name__icontains=keyword) |
                Q(brand__icontains=keyword) |
                Q(ingredients__name__icontains=keyword)
            ).distinct()

        if category:
            products = products.filter(category=category)

        if concern:
            products = products.filter(concerns=concern)

        if skin_type:
            products = products.filter(skin_types=skin_type)

        if feature:
            products = products.filter(features__name__icontains=feature).distinct()
            
    favorite_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'product_search.html', {
        'form': form,
        'products': products,
        'favorite_ids': list(favorite_ids),
    })


@login_required
def favorite_list_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'app/favorite_list.html', {'favorites': favorites})

@login_required
def add_favorite_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return redirect('product_search')

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

@login_required
def chat_user_list_view(request):
    user = request.user

    # アドバイザーだけがこの一覧を見られるように制限
    if not user.is_advisor:
        return redirect('chat')

    # このアドバイザーとやりとりしたことのあるユーザー一覧を取得
    user_ids = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).values_list('sender', 'receiver')

    # senderやreceiverにアドバイザー自身も含まれているので、自分を除外し、ユニークに
    other_user_ids = set()
    for sender_id, receiver_id in user_ids:
        if sender_id != user.id:
            other_user_ids.add(sender_id)
        if receiver_id != user.id:
            other_user_ids.add(receiver_id)

    users = CustomUser.objects.filter(id__in=other_user_ids)

    return render(request, 'chat_user_list.html', {'users': users})

@login_required
def chat_with_user_view(request, user_id):
    user = request.user

    # ログインユーザーがアドバイザーでなければ拒否
    if not user.is_advisor:
        return redirect('chat')

    # 相手ユーザーを取得
    chat_user = get_object_or_404(CustomUser, id=user_id)

    # このアドバイザーとユーザー間のメッセージのみ取得
    messages = Message.objects.filter(
        (Q(sender=user, receiver=chat_user) | Q(sender=chat_user, receiver=user))
    ).order_by('timestamp')

    # メッセージ送信処理（POST）
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=user, receiver=chat_user, content=content)
            return redirect('chat_with_user', user_id=chat_user.id)

    return render(request, 'chat_with_user.html', {
        'chat_user': chat_user,
        'messages': messages,
    })
    
@login_required
def advisor_unassigned_list(request):
    sessions = ChatSession.objects.filter(status='unassigned').order_by('-created_at')
    return render(request, 'advisor/unassigned_list.html', {'sessions': sessions})

@login_required
def user_skincare_record_list_view(request, user_id):
    advisor = request.user

    # アドバイザー以外はアクセス不可
    if not advisor.is_advisor:
        return redirect('home')

    # 対象ユーザーの記録を取得
    target_user = get_object_or_404(CustomUser, id=user_id)
    records = SkincareRecord.objects.filter(user=target_user).order_by('-record_date')

    return render(request, 'user_skincare_record_list.html', {
        'target_user': target_user,
        'records': records,
    })
 
@login_required
def user_record_calendar_view(request, user_id):
    if not request.user.is_advisor:
        return redirect('home')

    target_user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'user_record_calendar.html', {
        'target_user': target_user
    })

@login_required
def user_record_calendar_events_view(request, user_id):
    if not request.user.is_advisor:
        return JsonResponse([], safe=False)

    target_user = get_object_or_404(CustomUser, id=user_id)
    records = SkincareRecord.objects.filter(user=target_user)

    events = []
    for record in records:
        events.append({
            "title": "記録あり",
            "start": str(record.record_date),
            "url": f"/record/{record.pk}/detail/"
        })

    return JsonResponse(events, safe=False)

@login_required
def profile_view(request):
    user = request.user
    if user.is_advisor:
        return render(request, 'advisor/profile.html', {'user': user})
    else:
        return render(request, 'profile.html', {'user': user})

@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=user)
        account_form = UserEditForm(request.POST, instance=user)
        if profile_form.is_valid() and account_form.is_valid():
            profile_form.save()
            account_form.save()
            messages.success(request, 'プロフィールを更新しました。')
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=user)
        account_form = UserEditForm(instance=user)

    template_name = 'advisor/edit_profile.html' if user.is_advisor else 'edit_profile.html'

    return render(request, template_name, {
        'profile_form': profile_form,
        'account_form': account_form,
    })


User = get_user_model()

@login_required
def edit_account_view(request):
    user = request.user
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'アカウント情報を更新しました。')
            return redirect('profile')  # プロフィール画面に戻る
    else:
        form = EditAccountForm(instance=user)

    template_name = 'advisor/edit_account.html' if user.is_advisor else 'edit_account.html'

    return render(request, template_name, {'form': form})


@require_POST
@login_required
def toggle_favorite_ajax(request):
    product_id = request.POST.get('product_id')
    if not product_id:
        return JsonResponse({'success': False}, status=400)

    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if not created:
        # すでにお気に入り→削除する
        favorite.delete()
        return JsonResponse({'success': True, 'status': 'removed'})
    else:
        # 新規追加された
        return JsonResponse({'success': True, 'status': 'added'})
    
    
@require_POST
@login_required
def advisor_start_chat(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id)
    session.advisor = request.user
    session.status = 'active'
    session.started_at = timezone.now()
    session.save()
    return redirect('advisor_active_chats')  # ※このURLは後で作る「対応中」一覧ページ

@login_required
def advisor_active_chats(request):
    sessions = ChatSession.objects.filter(
        advisor=request.user,
        status='active'
    ).order_by('-started_at')
    return render(request, 'advisor/active_chats.html', {'sessions': sessions})

@login_required
@require_http_methods(["GET", "POST"])
def chat_session_detail(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id)

    # ログインユーザーがアドバイザー本人でなければアクセス拒否
    if request.user != session.advisor:
        return redirect('advisor_active_chats')

    # メッセージ送信処理
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                session=session,
                sender=request.user,
                receiver=session.user,  # 相手ユーザー
                content=content
            )
        return redirect('chat_session_detail', session_id=session.id)

    # すべてのメッセージを取得（このセッションに属する）
    messages = session.messages.order_by('timestamp')

    return render(request, 'advisor/chat_session_detail.html', {
        'session': session,
        'messages': messages,
    })
    
@require_POST
@login_required
def chat_session_complete(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id)
    if request.user != session.advisor:
        return redirect('advisor_active_chats')

    session.status = 'completed'
    session.ended_at = timezone.now()
    session.save()
    return redirect('advisor_active_chats')

@login_required
def advisor_completed_chats(request):
    sessions = ChatSession.objects.filter(
        advisor=request.user, status='completed'
    ).order_by('-ended_at')
    return render(request, 'advisor/completed_chats.html', {
        'sessions': sessions
    })

@login_required
def advisor_profile_view(request):
    return render(request, 'advisor/profile.html', {
        'user': request.user
    })
