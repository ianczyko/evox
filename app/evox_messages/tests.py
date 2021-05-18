from django.test import TestCase
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
        error_msg = message.validate_message()
        self.assertEqual(error_msg, None)

    def test_validate_message_empty(self):
        message = Message(content='')
        error_msg = message.validate_message()
        self.assertNotEqual(error_msg, None)

    def test_validate_message_too_long(self):
        msg_content = 'a' * 200
        message = Message(content=msg_content)
        error_msg = message.validate_message()
        self.assertNotEqual(error_msg, None)
