import json
from rest_framework_api_key.models import APIKey
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from evox_messages.models import Message


class MessageModelTestCase(TestCase):
    def setUp(self):
        Message.objects.create(content='msg1')
        Message.objects.create(content='msg2')

    def test_init(self):
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


class MessageAPIShowViewTestCase(TestCase):
    def setUp(self):
        Message.objects.create(content='msg1')

    def test_ok_status(self):
        response = self.client.get('/api/messages/1')
        self.assertEqual(response.status_code, 200)

    def test_nonexisting_id_status(self):
        response = self.client.get('/api/messages/5')
        self.assertEqual(response.status_code, 404)

    def test_not_allowed_method_status(self):
        response = self.client.post('/api/messages/1')
        self.assertEqual(response.status_code, 405)

    def test_response_content(self):
        response = self.client.get('/api/messages/1')
        message_obj_str = response.content.decode('utf-8')
        message_obj = json.loads(message_obj_str)
        message_content = message_obj['content']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message_content, 'msg1')


class MessageAPIEditMessageViewTestCase(TestCase):
    def setUp(self):
        Message.objects.create(content='msg1')
        _, key = APIKey.objects.create_key(name="test_key")
        self._api_key = f'Api-Key {key}'

    def test_ok_status(self):
        data = '{"content": "msg2"}'
        response = self.client.put(
            '/api/messages/1',
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION=self._api_key
        )
        self.assertEqual(response.status_code, 200)

    def test_no_auth_key_status(self):
        data = '{"content": "msg2"}'
        response = self.client.put(
            '/api/messages/1',
            data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)

    def test_wrong_auth_key_status(self):
        data = '{"content": "msg2"}'
        response = self.client.put(
            '/api/messages/1',
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION='secret123'
        )
        self.assertEqual(response.status_code, 403)

    def test_nonexisting_id_status(self):
        data = '{"content": "msg2"}'
        response = self.client.put(
            '/api/messages/5',
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION=self._api_key
        )
        self.assertEqual(response.status_code, 404)

    def test_not_allowed_method_status(self):
        data = '{"content": "msg2"}'
        response = self.client.post(
            '/api/messages/1',
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION=self._api_key
        )
        self.assertEqual(response.status_code, 405)

    def test_response_content(self):
        data = '{"content": "msg2"}'
        response = self.client.put(
            '/api/messages/1',
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION=self._api_key
        )
        message_obj_str = response.content.decode('utf-8')
        message_obj = json.loads(message_obj_str)
        message_content = message_obj['content']
        self.assertEqual(message_content, 'msg2')


class MessageAPINewViewTestCase(TestCase):
    def setUp(self):
        Message.objects.create(content='msg1')
        _, key = APIKey.objects.create_key(name="test_key")
        self._api_key = f'Api-Key {key}'

    def test_ok_status(self):
        data = '{"content": "msg2"}'
        response = self.client.post(
            '/api/messages/',
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION=self._api_key
        )
        self.assertEqual(response.status_code, 200)

    def test_no_auth_key_status(self):
        data = '{"content": "msg2"}'
        response = self.client.post(
            '/api/messages/',
            data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)

    def test_wrong_auth_key_status(self):
        data = '{"content": "msg2"}'
        response = self.client.post(
            '/api/messages/',
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION='secret123'
        )
        self.assertEqual(response.status_code, 403)

    def test_not_allowed_method_status(self):
        response = self.client.get('/api/messages/',)
        self.assertEqual(response.status_code, 405)

    def test_response_content(self):
        data = '{"content": "msg2"}'
        response = self.client.post(
            '/api/messages/',
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION=self._api_key
        )
        message_obj_str = response.content.decode('utf-8')
        message_obj = json.loads(message_obj_str)
        message_content = message_obj['content']
        self.assertEqual(message_content, 'msg2')


class MessageAPIDeleteViewTestCase(TestCase):
    def setUp(self):
        Message.objects.create(content='msg1')
        Message.objects.create(content='msg2')
        Message.objects.create(content='msg3')
        Message.objects.create(content='msg4')
        Message.objects.create(content='msg5')
        _, key = APIKey.objects.create_key(name="test_key")
        self._api_key = f'Api-Key {key}'

    def test_ok_status(self):
        response = self.client.delete(
            '/api/messages/1',
            HTTP_AUTHORIZATION=self._api_key
        )
        self.assertEqual(response.status_code, 200)

    def test_no_auth_key_status(self):
        response = self.client.delete(
            '/api/messages/2',
        )
        self.assertEqual(response.status_code, 403)

    def test_wrong_auth_key_status(self):
        response = self.client.delete(
            '/api/messages/3',
            HTTP_AUTHORIZATION='secret123'
        )
        self.assertEqual(response.status_code, 403)

    def test_not_allowed_method_status(self):
        data = '{"content": "msg2"}'
        response = self.client.post(
            '/api/messages/3',
            data,
            content_type='application/json',
            HTTP_AUTHORIZATION=self._api_key
        )
        self.assertEqual(response.status_code, 405)

    def test_response_content(self):
        response = self.client.delete(
            '/api/messages/4',
            HTTP_AUTHORIZATION=self._api_key
        )
        message_obj_str = response.content.decode('utf-8')
        message_obj = json.loads(message_obj_str)
        message_content = message_obj['content']
        self.assertEqual(message_content, 'msg4')
