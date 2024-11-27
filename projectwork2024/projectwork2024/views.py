from django.shortcuts import render

def chat_interface(request):
    question = request.GET.get('question', '')  # Получаем вопрос из параметров запроса (если есть)
    context = {'question': question}  # Передаём вопрос в шаблон
    return render(request, 'chat.html', context)  # Рендерим шаблон chat.html