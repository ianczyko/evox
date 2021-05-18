from django.forms import model_to_dict
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework_api_key.permissions import HasAPIKey
from evox_messages.models import Message


@api_view(['GET'])
def message_show(request, id: int):
    message = model_to_dict(Message.objects.get(pk=id))
    return JsonResponse(message)


@api_view(['GET'])
@permission_classes([HasAPIKey])
def message_edit(request, id: int):
    return HttpResponse(f'Edit message with id={id}')


@api_view(['GET'])
@permission_classes([HasAPIKey])
def message_delete(request, id: int):
    return HttpResponse(f'Edit message with id={id}')


@api_view(['GET'])
@permission_classes([HasAPIKey])
def message_new(request):
    return HttpResponse('Create new message')
