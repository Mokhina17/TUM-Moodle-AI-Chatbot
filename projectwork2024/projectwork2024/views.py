from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserInput
import json

def chat_interface(request):
    return render(request, 'chat.html')

@csrf_exempt  # Temporarily disable CSRF for testing (not recommended in production)
def process_input(request):
    if request.method == 'POST':
        try:
            # Load the JSON data from the request body
            body = json.loads(request.body)
            user_input = body.get('user_input')

            if not user_input:
                return JsonResponse({'error': 'No user input provided'}, status=400)

            # Try saving the user input to the database
            new_input = UserInput.objects.create(user_input=user_input)

            return JsonResponse({'message': f"Input saved with ID: {new_input.id}"})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        except Exception as e:
            # Log the exception to check what went wrong
            print(f"Error processing input: {e}")
            return JsonResponse({'error': f"An unexpected error occurred: {str(e)}"}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
