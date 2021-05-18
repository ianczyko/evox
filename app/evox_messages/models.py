from django.db import models
from django.core.exceptions import ValidationError


class Message(models.Model):
    content = models.CharField(max_length=160)
    view_count = models.IntegerField(default=0)
    # id is added automatically

    def validate_message(self):
        try:
            self.clean_fields()
            error_msg = None
        except ValidationError as e:
            p_output = e.message_dict['content'][0]
            error_msg = {
                'detail': f'Malformed message. Parser output: {p_output}'
            }
        return error_msg
