from django.test import TestCase
from evox_messages.models import Message


class MessageModelTestCase(TestCase):
    def setUp(self):
        Message.objects.create(content='msg1')
        Message.objects.create(content='msg2')

    def test_id_incremented_create(self):
        """Message model creation"""
        msg1 = Message.objects.get(pk=1)
        msg2 = Message.objects.get(pk=2)
        self.assertEqual(msg1.content, 'msg1')
        self.assertEqual(msg1.view_count, 0)
        self.assertEqual(msg2.content, 'msg2')
        self.assertEqual(msg2.view_count, 0)
