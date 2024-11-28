from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserInput
import json

def chat_interface(request):
    question = request.GET.get('question', '')
    context = {'question': question}
    return render(request, 'chat.html', context)