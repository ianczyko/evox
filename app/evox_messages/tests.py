from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from evox_messages.models import Message


class MessageModelTestCase(TestCase):
    def setUp(self):
        Message.objects.create(content='msg1')
        Message.objects.create(content='msg2')

    def test_init(self):
        """Message model creation"""
        msg1 = Message.objects.get(pk=1)
        msg2 = Message.objects.get(pk=2)
        self.assertEqual(msg1.content, 'msg1')
        self.assertEqual(msg1.view_count, 0)
        self.assertEqual(msg2.content, 'msg2')
        self.assertEqual(msg2.view_count, 0)

    def test_validate_message_valid(self):
        message = Message(content='msg1')
        message.validate_message()
        self.assertEqual(message.content, 'msg1')

    def test_validate_message_empty(self):
        message = Message(content='')
        self.assertRaises(ValidationError, message.validate_message)

    def test_validate_message_too_long(self):
        msg_content = 'a' * 200
        message = Message(content=msg_content)
        self.assertRaises(ValidationError, message.validate_message)

    def test_retrieve_by_id_success(self):
        message = Message.retrieve_by_id(1)
        self.assertEqual(message.content, 'msg1')

    def test_retrieve_by_id_fail(self):
        self.assertRaises(ObjectDoesNotExist, Message.retrieve_by_id, id=5)
