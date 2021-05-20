import json
from json.decoder import JSONDecodeError
from django.forms import model_to_dict
from django.db.models import F
from django.http.response import JsonResponse
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework import status
from evox_messages.models import Message


@api_view(['GET', 'PUT', 'DELETE'])
def message_dispatcher(request, id: int):
    if request.method == 'GET':
        return message_show(request._request, id)
    if request.method == 'PUT':
        return message_edit(request._request, id)
    if request.method == 'DELETE':
        return message_delete(request._request, id)


@api_view(['GET'])
def message_show(request, id: int):
    try:
        message = Message.retrieve_by_id(id)
        # Save and return message before updating:
        # Needed due to the use of F expression
        # Pros: atomic incrementation, resolved race conditions
        # Cons: displayed counter does not include the current call
        output = model_to_dict(message)
        message.view_count = F('view_count') + 1
        message.save(update_fields=['view_count'])
        return JsonResponse(output)
    except ObjectDoesNotExist as e:
        short = f'Message with id #{id} has not been found.'
        detail = str(e)
        err_status = status.HTTP_404_NOT_FOUND
    return error_response(short, detail, err_status)


@api_view(['PUT'])
@permission_classes([HasAPIKey])
def message_edit(request, id: int):
    try:
        request_body = request.body.decode('utf-8')
        message_obj = json.loads(request_body)
        message_content = message_obj['message']
        message = Message.retrieve_by_id(id)
        message.content = message_content
        message.view_count = 0
        message.validate_message()
        message.save()
        output = model_to_dict(message)
        return JsonResponse(output)
    except JSONDecodeError as e:
        short = 'Could not validate JSON.'
        detail = str(e)
        err_status = status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        short = 'Message field not found.'
        detail = str(e)
        err_status = status.HTTP_400_BAD_REQUEST
    except ValidationError as e:
        short = 'Message validation failed.'
        detail = e.message_dict['content'][0]
        err_status = status.HTTP_422_UNPROCESSABLE_ENTITY
    return error_response(short, detail, err_status)


@api_view(['DELETE'])
@permission_classes([HasAPIKey])
def message_delete(request, id: int):
    try:
        message = Message.retrieve_by_id(id)
        output = model_to_dict(message)
        message.delete()
        return JsonResponse(output)
    except ObjectDoesNotExist as e:
        short = f'Message with id #{id} has not been found.'
        detail = str(e)
        err_status = status.HTTP_404_NOT_FOUND
    return error_response(short, detail, err_status)


@api_view(['POST'])
@permission_classes([HasAPIKey])
def message_new(request):
    try:
        request_body = request.body.decode('utf-8')
        message_obj = json.loads(request_body)
        message_content = message_obj['message']
        message = Message(content=message_content)
        message.validate_message()
        message.save()
        output = model_to_dict(message)
        return JsonResponse(output)
    except JSONDecodeError as e:
        short = 'Could not validate JSON.'
        detail = str(e)
        err_status = status.HTTP_400_BAD_REQUEST
    except KeyError as e:
        short = 'Message field not found.'
        detail = str(e)
        err_status = status.HTTP_400_BAD_REQUEST
    except ValidationError as e:
        short = 'Message validation failed.'
        detail = e.message_dict['content'][0]
        err_status = status.HTTP_422_UNPROCESSABLE_ENTITY
    return error_response(short, detail, err_status)


def error_response(short, detail, err_status):
    return JsonResponse({
        'error': {
            'short': short,
            'detail': detail,
        }
    }, status=err_status)
