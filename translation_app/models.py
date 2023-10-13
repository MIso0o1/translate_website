from django.db import models
from django.contrib.auth.models import User

class TranslatedFile(models.Model):
    translated_file = models.FileField(upload_to='translations/')
    target_language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    class Meta:
        app_label = 'translation_app'

    def __str__(self):
        return f"Translated File ({self.original_file.name})"
