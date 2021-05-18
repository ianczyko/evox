from django.forms import model_to_dict
from django.db.models import F
from django.http.response import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework import status
from rest_framework.response import Response
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
    message = Message.objects.get(pk=id)
    # Save and return message before updating:
    # Needed due to the use of F expression
    # Pros: atomic incrementation, resolved race conditions
    # Cons: displayed counter does not include the current call
    output = model_to_dict(message)
    message.view_count = F('view_count') + 1
    message.save(update_fields=['view_count'])
    return JsonResponse(output)


@api_view(['PUT'])
@permission_classes([HasAPIKey])
def message_edit(request, id: int):
    message_content = request.body.decode('utf-8')
    message = Message.objects.get(pk=id)
    message.content = message_content
    message.view_count = 0
    try:
        message.clean_fields()
    except ValidationError as e:
        error_msg = {'detail': 'Malformed message. Parser output: '}
        error_msg['detail'] += e.message_dict['content'][0]
        return Response(error_msg, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    message.save()
    output = model_to_dict(message)
    return JsonResponse(output)


@api_view(['DELETE'])
@permission_classes([HasAPIKey])
def message_delete(request, id: int):
    message = Message.objects.get(pk=id)
    output = model_to_dict(message)
    message.delete()
    return JsonResponse(output)


@api_view(['POST'])
@permission_classes([HasAPIKey])
def message_new(request):
    message_content = request.body.decode('utf-8')
    message = Message(content=message_content)
    try:
        message.clean_fields()
    except ValidationError as e:
        error_msg = {'detail': 'Malformed message. Parser output: '}
        error_msg['detail'] += e.message_dict['content'][0]
        return Response(error_msg, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    message.save()
    output = model_to_dict(message)
    return JsonResponse(output)
