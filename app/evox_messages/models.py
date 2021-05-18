from django.db import models


class Message(models.Model):
    content = models.CharField(max_length=160)
    view_count = models.IntegerField(default=0)
    # id is added automatically
