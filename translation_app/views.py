import requests
import base64
import json
from django.http import HttpResponse
from .forms import TranslationForm
from .models import TranslatedFile  # Import your model if not already imported

# Define the API endpoint URL (replace with your actual API URL)
api_url = "https://translate-documents-79a700ed9476.herokuapp.com/translate"

def upload_file(request):
    if request.method == 'POST':
        form = TranslationForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the target language and uploaded file from the form
            target_language = form.cleaned_data['target_language']
            uploaded_file = request.FILES['file']

            # Prepare headers for the API request
            api_key = "e5a24b06799b3bdda926f26ee68594d6"  # Replace with your API key
            headers = {"X-API-Key": api_key}

            # Define the payload with language
            payload = {"language": target_language}

            # Define the files to be sent in form-data
            files = {"file": (uploaded_file.name, uploaded_file.read())}

            # Make the POST request to the translation API
            response = requests.post(api_url, headers=headers, data=payload, files=files)

            if response.status_code == 200:
                # Parse the JSON response
                response_data = json.loads(response.text)

                # Extract the base64 string from the "translated_content" field
                base64_string = response_data.get("translated_content", "")

                if base64_string:
                    # Decode the base64 string to bytes
                    decoded_bytes = base64.b64decode(base64_string)

                    # Set the content type for the response
                    response = HttpResponse(decoded_bytes, content_type="application/octet-stream")

                    # Set the content-disposition header to trigger a download
                    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.name}"'

                    return response

                else:
                    return HttpResponse("Base64 string not found in the response.")

            else:
                return HttpResponse(f"Translation failed. Status Code: {response.status_code}")

    else:
        form = TranslationForm()

    return render(request, 'translation_app/upload_file.html', {'form': form})
