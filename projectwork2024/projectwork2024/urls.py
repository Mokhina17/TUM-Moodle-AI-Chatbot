"""
URL configuration for projectwork2024 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from projectwork2024.views import chat_interface, chat_response, load_chat, start_new_chat
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', chat_interface, name='home'),  # Default route
    path('chat_response/', chat_response, name='chat_response'),
    path('chat/load/<int:chat_id>/', load_chat, name='load_chat'),
    path('start_new_chat/', start_new_chat, name='start_new_chat'),
]
