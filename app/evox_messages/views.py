from django.http import HttpResponse


def messages(request):
    return HttpResponse('Return all messages')


def message_edit(request, id: int):
    return HttpResponse(f'Edit message with id={id}')


def message_delete(request, id: int):
    return HttpResponse(f'Edit message with id={id}')


def message_new(request):
    return HttpResponse('Create new message')
