from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .DocStore import DocStore
from .Integration import Phi35Instruct
import json

# Initialize DocStore and Phi35Instruct
doc_store = DocStore()
phi_model = Phi35Instruct()

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
        
        # Generate response using SmolLM
        response = phi_model.generate_response(user_query,relevant_docs)
        
        # Prepare the response data
        response_data = {
            'user_query': user_query,
            'response': response,
            'relevant_docs': [doc for doc, _ in relevant_docs]
        }
        
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request method'}, status=400)