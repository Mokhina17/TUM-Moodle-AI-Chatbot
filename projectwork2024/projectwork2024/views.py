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
        try:
            data = json.loads(request.body)
            user_query = data.get('user_query')

            if not user_query:
                return JsonResponse({'error': 'User query is required'}, status=400)

            # Retrieve relevant documents
            relevant_docs = doc_store.search(user_query, k=5)

            if not relevant_docs:
                return JsonResponse({'error': 'No relevant documents found'}, status=404)

            # Generate response using model
            response = model.generate_response(user_query, relevant_docs)

            # Prepare the response data
            response_data = {
                'user_query': user_query,
                'response': response,
                'relevant_docs': [doc[:200] + '...' for doc, _ in relevant_docs],  # Truncate docs
            }
            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
