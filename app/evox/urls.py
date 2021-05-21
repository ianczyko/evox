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
from evox_messages.views import message_dispatcher


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/messages/', message_dispatcher),
    path('api/messages/<int:id>', message_dispatcher),
]

handler400 = 'evox_messages.views.bad_request'
handler403 = 'evox_messages.views.permission_denied'
handler404 = 'evox_messages.views.page_not_found'
handler500 = 'evox_messages.views.server_error'
