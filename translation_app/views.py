




import requests
from django.shortcuts import render
from django.http import HttpResponse
from .forms import TranslationForm
from .models import TranslatedFile  # Import your model if not already imported
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 

# Define the API endpoint URL (replace with your actual API URL)
api_url = "https://translate-documents-79a700ed9476.herokuapp.com/translate"

@login_required  # Use the login_required decorator to ensure the user is logged in
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

            # Define the payload with language and file
            payload = {"language": target_language}  # Replace with the target language code

            # Define the files to be sent in form-data
            files = {"file": (uploaded_file.name, uploaded_file.read())}

            # Send the POST request to the translation API
            response = requests.post(api_url, headers=headers, data=payload, files=files)

            if response.status_code == 200:
                # Translation successful
                translated_content = response.text

                # Create a TranslatedFile object and save it to the database
                user = request.user  # Get the currently logged-in user
                translated_file = TranslatedFile(
                    user=user,  # Associate the user with the file
                    original_file=uploaded_file,
                    translated_file=translated_content,
                    target_language=target_language,
                )
                translated_file.save()

                # Render the translated content in a template
                return render(request, 'translation_app/translated_result.html', {'translated_content': translated_content})

            else:
                # Translation failed; handle the error
                return HttpResponse(f"Translation failed. Status Code: {response.status_code}")

    else:
        form = TranslationForm()

    return render(request, 'translation_app/upload_file.html', {'form': form})
