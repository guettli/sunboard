from random import randint

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html

from sunboard.htmlutils import empty_page, join, HTTPResponseHXRedirect
from sunboard.models import Board, Item


def add_item(request):
    assert 0

def start_page(request):
    return empty_page(format_html('<button hx-post="{create_board_url}">Create new Sunboard</button>',
                      create_board_url=reverse('create_board_page')))

def create_board_page(request):
    board = Board.objects.create()
    return HTTPResponseHXRedirect(board.get_absolute_url())

def board_page(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    return empty_page(format_html('''
    <h1>{title}</h1>
    {items}
    <button hx-post="{add_item_url}" hx-swap="afterend" style="position: fixed; bottom: 0px">+</button>
    ''', title=board.title, items=join(item_html(item) for item in Item.objects.filter(board=board)),
                                  add_item_url=reverse('add_item_hx', kwargs=dict(board_id=board_id))
                                  ))

def item_html(item):
    return format_html('''<div class="item-border-div draggable " style="left: {x}em; top: {y}em"><textarea class="item">{text}</textarea></div>''',
                       text=item.text, x=item.x, y=item.y)

def add_item_hx(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    item = Item.objects.create(board=board, x=randint(10, 20), y=randint(10, 20))
    return HttpResponse(item_html(item))

