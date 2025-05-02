from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class LettersAndNumbersValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(_('パスワードは8文字以上である必要があります。'))

        if not re.search(r'[a-zA-Z]', password):
            raise ValidationError(_('パスワードには英字を1文字以上含めてください。'))

        if not re.search(r'\d', password):
            raise ValidationError(_('パスワードには数字を1文字以上含めてください。'))

    def get_help_text(self):
        return _('パスワードには英字と数字を含め、8文字以上にしてください。')
