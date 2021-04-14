import re
import sys
from django.templatetags.static import static

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Context
from django.template import Template
from django.urls import reverse, path
from django.utils.formats import number_format
from django.utils.html import conditional_escape
from django.utils.html import format_html
from django.utils.safestring import mark_safe, SafeString
from django_middleware_global_request.middleware import (
    get_request,
)


def join(my_list, sep='', type=None, empty_text=''):
    if not my_list:
        return empty_text
    if type is None:
        return mark_safe(sep.join([conditional_escape(item) for item in my_list]))
    if type == 'ul':
        return format_html(
            '<ul>{}</ul>', join([format_html('<li>{}</li>', item) for item in my_list])
        )
    raise Exception(f'Unknown type {type}')


class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['HX-Redirect'] = self['Location']

    status_code = 200


def alert_div(msg):
    return format_html(
        '''<div class="alert alert-warning" role="alert">{}</div>''', msg
    )


def empty_page(content):
    return HttpResponse(format_html('''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
    <link href="{sunboard_css}" rel="stylesheet">
    <title>🌞 Sunboard 🌞</title>
  </head>
  <body>
    <h1>🌞 Sunboard 🌞</h1>
    {content}
    <script src="https://unpkg.com/htmx.org@1.3.3/dist/htmx.min.js" integrity="sha384-QrlPmoLqMVfnV4lzjmvamY0Sv/Am8ca1W7veO++Sp6PiIGixqkD+0xZ955Nc03qO" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/interactjs@1.10.11/dist/interact.min.js" integrity="sha384-LqpTUp2dBNxqY7IYl4r0m6IegZjlkQgpMo6VAoHYgLTewlETlLaHd3DfywaLNy9J" crossorigin="anonymous"></script>
    <script src="{sunboard_js}"></script>
  </body>
</html>''', content=content, sunboard_css=static('sunboard/sunboard.css'),
                                    sunboard_js=static('sunboard/sunboard.js')))


def link(obj):
    if isinstance(obj, User):
        url = reverse('user_profile_page', kwargs=dict(user_id=obj.id))
    else:
        url = obj.get_absolute_url()
    return format_html('<a href="{}">{}</a>', url, obj)

def list_to_html_list(items, type='ul', li_style=''):
    new = []
    if li_style:
        li_style = format_html(' style="{li_style}"', li_style=li_style)
    for item in items:
        item = item.strip()
        if not item:
            continue
        new.append(
            format_html('<li{li_style}>{item}</li>', li_style=li_style, item=item)
        )
    if not new:
        return ''
    return format_html('<{type}>{items}</{type}>', type=type, items=join(new))




def short_path(method):
    """
    short_path() is wrapper for path().

    But, I think a different approach would be better:
    No manual url.py entries: Instead do a mapping from URL to file-name.
    This way the pages can be loaded on demand (lazy).
    """
    assert method.__name__.endswith('_page') or method.__name__.endswith('_cronpage')
    short = method.__name__[:-5]
    return path(f'{short}', method, name=method.__name__)


def base_url():
    domain = Site.objects.get_current().domain
    if domain.startswith('127'):
        proto = 'http'
    else:
        proto = 'https'
    return f'{proto}://{domain}'


def admin_link(obj, text=None):
    if obj is None:
        return ''
    if text is None:
        text = str(obj)
    return format_html(
        '<a href="{}">{}</a>',
        reverse(
            f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=(obj.id,)
        ),
        text,
    )


def session_message(message, level=messages.INFO):
    request = get_request()
    if request is None:
        return
    messages.add_message(request, level, message)
