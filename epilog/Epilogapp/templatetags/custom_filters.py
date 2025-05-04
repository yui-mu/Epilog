from django import template

register = template.Library()

@register.filter
def split(value, delimiter=","):
    return value.split(delimiter)

@register.filter
def expertise_label(value):
    labels = {
        'type': '肌タイプ別の専門分野',
        'concern': '肌悩み別の専門分野',
        'method': 'スキンケア手順・方法に関する専門分野',
        'ingredient': '成分に関する専門分野',
    }
    return labels.get(value.strip(), value)
