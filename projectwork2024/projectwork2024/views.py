from django.shortcuts import render

def chat_interface(request):
    return render(request, 'chat.html')