from uuid import uuid4

from django.db import models
from django.urls import reverse


class Board(models.Model):
    id = models.UUIDField(primary_key= True, default=uuid4())
    title = models.CharField(max_length=64, default='Sunboard')

    def get_absolute_url(self):
        return reverse('board_page', kwargs=dict(board_id=self.id))

class Item(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    text = models.TextField(default='')
    x = models.SmallIntegerField()
    y = models.SmallIntegerField()
    z = models.SmallIntegerField(default=0)

