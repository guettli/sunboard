from django.urls import path

from sunboard.views import start_page, board_page, create_board_page, add_item_hx

urlpatterns = [
    path('', start_page, name='start_page'),
    path('create_board_page', create_board_page, name='create_board_page'),
    path('board_page/<board_id>', board_page, name='board_page'),
    path('add_item_hx/<board_id>', add_item_hx, name='add_item_hx'),
]