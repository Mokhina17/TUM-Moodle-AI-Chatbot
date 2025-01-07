from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .DocStore import DocStore
from .Integration import Model
from .models import Conversation
import json

# Initialize DocStore and Model
doc_store = DocStore()
model = Model()


def chat_interface(request):
    """Render the chatbot interface page."""
    question = request.GET.get('question', '')
    context = {'question': question}
    return render(request, 'chat.html', context)


@csrf_exempt
def chat_response(request):
    """Handle user queries and generate bot responses."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_query = data.get('user_query')

            if not user_query:
                return JsonResponse({'error': 'User query is empty.'}, status=400)

            # Retrieve relevant documents
            relevant_docs = doc_store.search(user_query, k=10)

            # Generate response using the model
            response = model.generate_response(user_query, relevant_docs)

            # Save user query and bot response
            session_id = request.session.session_key or request.session.create()
            Conversation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_id=session_id,
                message=user_query,
                sender='user'
            )
            Conversation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_id=session_id,
                message=response,
                sender='bot'
            )

            # Prepare and return response
            response_data = {
                'user_query': user_query,
                'response': response,
                'relevant_docs': [doc for doc, _ in relevant_docs]
            }
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)



def start_new_chat(request):
    """Clear chat history and start a new session."""
    if request.method == 'POST':
        request.session['chat_history'] = []
        request.session.modified = True
        return JsonResponse({'message': 'New chat started successfully.'})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def load_chat(request, chat_id):
    """Load a specific chat by its ID."""
    try:
        conversation = Conversation.objects.filter(id=chat_id).order_by('timestamp')
        messages = [{'sender': msg.sender, 'message': msg.message, 'timestamp': msg.timestamp} for msg in conversation]
        return JsonResponse({'messages': messages})
    except Conversation.DoesNotExist:
        return JsonResponse({'error': 'Chat not found.'}, status=404)
