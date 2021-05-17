"""evox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from evox_messages.views import (
    messages,
    message_edit,
    message_new,
    message_delete
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/messages/new', message_new),
    path('api/messages/<int:id>/edit', message_edit),
    path('api/messages/<int:id>/delete', message_delete),
    path('api/messages/', messages),
]
