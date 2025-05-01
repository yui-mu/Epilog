from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

RATING_CHOICES = [
        (1, 'とても良い'),
        (2, '良い'),
        (3, '普通'),
        (4, 'やや悪い'),
        (5, '悪い'),
    ]
SKIN_CONCERN_CHOICES = [
    ('dry', '乾燥'),
    ('dull', 'くすみ'),
    ('wrinkle', 'シワたるみ'),
    ('spot', 'シミ'),
    ('pore', '毛穴'),
    ('acne', '赤み・ニキビ'),
]



class CustomUser(AbstractUser):
    email = models.EmailField("メールアドレス", unique=True)
    nickname = models.CharField("ニックネーム", max_length=64)
    username = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='ユーザー名',
        help_text='30文字以下で入力してください。英数字と @/./+/-/_ が使えます。',
        error_messages={
            'unique': "このユーザー名は既に使用されています。",
        },
    )
    is_advisor = models.BooleanField("アドバイザーかどうか", default=False)
    age = models.PositiveIntegerField("年齢", null=True, blank=True)  
    profile_photo = models.ImageField("プロフィール写真", upload_to='profile_photos/', null=True, blank=True)
    concerns = models.ManyToManyField('Concern', blank=True, verbose_name="肌悩み")  
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)
    
    
    USERNAME_FIELD = 'email'  # ← これで「email」でログインするようになる
    REQUIRED_FIELDS = ['username']  # 管理コマンド用に必要なフィールド



    def __str__(self):
        return self.username

    
class SkincareRecord(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    record_date = models.DateField("記録日")
    skin_condition = models.TextField("肌の状態メモ", blank=True)
    skin_rating = models.IntegerField("肌の調子", choices=RATING_CHOICES)
    photo = models.ImageField("肌の写真", upload_to='photos/', blank=True, null=True)
    
    morning_items = models.TextField("朝の使用アイテム", blank=True)
    night_items = models.TextField("夜の使用アイテム", blank=True)
    concerns = models.TextField("肌悩み", blank=True)
    ingredients = models.TextField("気になる成分", blank=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} の記録（{self.record_date}）"

# 成分モデル
class Ingredient(models.Model):
    name = models.CharField("成分名", max_length=100)

    def __str__(self):
        return self.name

# 肌悩みモデル
class Concern(models.Model):
    name = models.CharField("肌悩み", max_length=100)

    def __str__(self):
        return self.name

# 商品モデル
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('クレンジング', 'クレンジング'),
        ('洗顔', '洗顔'),
        ('化粧水', '化粧水'),
        ('乳液', '乳液'),
        ('美容液', '美容液'),
        ('クリーム', 'クリーム'),
        
        # 必要に応じてさらに追加
    ]

    name = models.CharField("商品名", max_length=200)
    brand = models.CharField("ブランド名", max_length=100)
    category = models.CharField("カテゴリ", max_length=100, choices=CATEGORY_CHOICES)
    
    image = models.ImageField("商品画像", upload_to='photos/', blank=True, null=True)

    ingredients = models.ManyToManyField(Ingredient, blank=True, verbose_name="配合成分")
    concerns = models.ManyToManyField(Concern, blank=True, verbose_name="対応する肌悩み")
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return f"{self.name}（{self.brand}）"
    
class SkinType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} ❤️ {self.product.name}"
    
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receiver = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='received_messages',
    null=True  
)
    content = models.TextField("メッセージ内容")
    timestamp = models.DateTimeField("送信日時", auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"



