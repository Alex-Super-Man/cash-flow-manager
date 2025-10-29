from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Возвращает закодированные параметры URL, которые совместимы с текущими параметрами запроса,
    обновляя только те параметры, которые переданы в тег.
    
    Например, если текущий URL: /transactions/?page=2&status=1
    {% param_replace page=3 %} вернет: page=3&status=1
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

@register.filter
def format_currency(value):
    """Форматирует число как денежную сумму"""
    try:
        return f"{float(value):,.2f}".replace(',', ' ').replace('.', ',')
    except (ValueError, TypeError):
        return value

@register.filter
def get_item(dictionary, key):
    """Возвращает значение из словаря по ключу"""
    return dictionary.get(key)

@register.filter
def add_class(field, css_class):
    """Добавляет CSS класс к полю формы"""
    return field.as_widget(attrs={"class": css_class})