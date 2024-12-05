from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .DocStore import DocStore
from .Integration import Model
import json


# Initialize DocStore and Model
doc_store = DocStore()
model = Model()

def chat_interface(request):
    question = request.GET.get('question', '')
    context = {'question': question}
    return render(request, 'chat.html', context)

@csrf_exempt
def chat_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_query = data.get('user_query')
        
        # Retrieve relevant documents using RAG
        relevant_docs = doc_store.search(user_query, k=1)
        
        # Generate response using model
        response = model.generate_response(user_query,relevant_docs)
        
        # Prepare the response data
        response_data = {
            'user_query': user_query,
            'response': response,
            'relevant_docs': [doc for doc, _ in relevant_docs]
        }
        
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def start_new_chat(request):
    if request.method == 'POST':
        # Logic to start a new chat (e.g., clear session or reset chat state)
        request.session['chat_history'] = []  # Example: clear chat history
        return JsonResponse({'message': 'New chat started successfully.'})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)