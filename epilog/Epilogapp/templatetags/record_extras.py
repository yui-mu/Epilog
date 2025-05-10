from django import template

register = template.Library()

@register.filter
def parse_items(value):
    """
    'カテゴリ:商品名:成分, カテゴリ:商品名:成分' を [
        {'category': ..., 'name': ..., 'ingredient': ...}, ...
    ] の形式にする
    """
    result = []
    for item in value.split(','):
        parts = [p.strip() for p in item.strip().split(':')]
        if len(parts) == 3:
            result.append({'category': parts[0], 'name': parts[1], 'ingredient': parts[2]})
        elif len(parts) == 2:
            result.append({'category': parts[0], 'name': parts[1], 'ingredient': ''})
        elif len(parts) == 1:
            result.append({'category': '', 'name': parts[0], 'ingredient': ''})
    return result
