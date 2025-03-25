from django.db import models

class AudioTranscription(models.Model):
    audio_file = models.FileField(upload_to='audio/')
    transcription = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audio Transcription {self.id}"