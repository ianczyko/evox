from django.db import models


class Message(models.Model):
    content = models.CharField(max_length=160)
    view_count = models.IntegerField(default=0)
    # id is added automatically

    def validate_message(self):
        self.clean_fields()

    @classmethod
    def retrieve_by_id(cls, id: int):
        message = cls.objects.get(pk=id)
        return message
