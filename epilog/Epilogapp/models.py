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
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} の記録（{self.record_date}）"


