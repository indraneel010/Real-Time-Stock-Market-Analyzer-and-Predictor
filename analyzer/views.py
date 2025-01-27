from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Placeholder for your ML model
def load_model():
    return "Your ML model here"

model = load_model()

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prediction = model  # Replace with actual prediction logic
            return JsonResponse({'prediction': prediction})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'message': 'Invalid request'}, status=405)
