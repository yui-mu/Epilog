from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    nickname = models.CharField("ニックネーム", max_length=64)
    is_advisor = models.BooleanField("アドバイザーかどうか", default=False)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return self.username
    
class SkincareRecord(models.Model):
    RATING_CHOICES = [
        (1, 'とても良い'),
        (2, '良い'),
        (3, '普通'),
        (4, 'やや悪い'),
        (5, '悪い'),
    ]

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
    name = models.CharField("商品名", max_length=200)
    brand = models.CharField("ブランド名", max_length=100)
    category = models.CharField("カテゴリ", max_length=100)

    ingredients = models.ManyToManyField(Ingredient, blank=True, verbose_name="配合成分")
    concerns = models.ManyToManyField(Concern, blank=True, verbose_name="対応する肌悩み")
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return f"{self.name}（{self.brand}）"

