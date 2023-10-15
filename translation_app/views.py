import requests
import base64
import json
from django.http import HttpResponse
from .forms import TranslationForm
from .models import TranslatedFile  # Import your model if not already imported
from django.shortcuts import render, redirect
import os
from django.shortcuts import render
from pdf2docx import Converter

# Define the API endpoint URL (replace with your actual API URL)
api_url = "https://translate-documents-79a700ed9476.herokuapp.com/translate"


# Function to convert PDF to Word and return the converted file to the user
import os
from django.http import HttpResponse
from django.shortcuts import render
from pdf2docx import Converter

# Function to convert PDF to Word and return the converted file to the user
def convert_to_word(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']

        # Save the uploaded PDF file in a designated location
        pdf_file_path = f'media/{pdf_file.name}'  # Adjust the path as per your project structure
        with open(pdf_file_path, 'wb+') as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)

        temp_docx_path = 'media/temp.docx'  # Temporary file path for the converted Word document

        # Convert the PDF file to Word
        cv = Converter(pdf_file_path)
        cv.convert(temp_docx_path)
        cv.close()

        # Read the content of the converted Word document
        with open(temp_docx_path, 'rb') as file:
            word_content = file.read()

        # Delete the temporary Word document
        os.remove(temp_docx_path)

        # Delete the PDF file from the media folder
        os.remove(pdf_file_path)

        # Set the content type for the response
        response = HttpResponse(word_content, content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        # Set the content-disposition header to trigger a download
        response['Content-Disposition'] = 'attachment; filename="converted_document.docx"'
        return response
    else:
        return HttpResponse("Error: No file uploaded.")


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
