from django import template

register = template.Library()


@register.filter
def add_class(field, css_class):
    """Agrega una clase CSS al widget del campo."""
    return field.as_widget(attrs={
        'class': f"{field.field.widget.attrs.get('class', '')} {css_class}".strip()
    })


@register.filter
def field_class(field):
    """
    Devuelve 'is-invalid' si el campo tiene errores, '' si no.
    Uso: {{ form.nombre|field_class }}
    """
    return 'is-invalid' if field.errors else ''

from django import template

register = template.Library()

@register.filter
def con_error(field):
    """Agrega is-invalid al campo si tiene errores de validación."""
    widget_class = field.field.widget.attrs.get('class', '')
    if field.errors:
        nueva_clase = f"{widget_class} is-invalid".strip()
    else:
        nueva_clase = widget_class
    return field.as_widget(attrs={'class': nueva_clase})