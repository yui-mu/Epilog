from django.core.exceptions import ValidationError
import re

def validate_password_contains_letters_and_numbers(password, user=None):
    if len(password) < 8:
        raise ValidationError('パスワードは8文字以上である必要があります。')

    if not re.search(r'[a-zA-Z]', password):
        raise ValidationError('パスワードには英字を1文字以上含めてください。')

    if not re.search(r'\d', password):
        raise ValidationError('パスワードには数字を1文字以上含めてください。')
