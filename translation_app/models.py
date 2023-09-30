from django.db import models

class TranslatedFile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    original_file = models.FileField(upload_to='uploads/')
    translated_file = models.FileField(upload_to='translations/')
    target_language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = 'translation_app'

    def __str__(self):
        return f"Translated File ({self.original_file.name})"
