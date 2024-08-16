from pos_system import templates
from pos_system.templates.defaultfilters import stringfilter
import markdown as md


register = template.Library()


@register.filter()


@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])
