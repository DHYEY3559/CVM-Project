from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .models import AudioTranscription
import whisper
import torch
import os
import sounddevice as sd
from scipy.io.wavfile import write
from django.http import JsonResponse

# Load the Whisper model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base").to(device)

def home(request):
    return render(request, 'stt_app/home.html')

def record_audio(request):
    if request.method == 'POST':
        duration = int(request.POST.get('duration', 10))
        sample_rate = 48000
        output_file = "recorded_audio.wav"

        print("Recording...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
        sd.wait()
        write(output_file, sample_rate, audio)

        # Save the recorded audio to the database
        with open(output_file, 'rb') as f:
            audio_transcription = AudioTranscription()
            audio_transcription.audio_file.save(output_file, ContentFile(f.read()))
            audio_transcription.save()

        # Transcribe the audio
        transcription = transcribe_audio(audio_transcription.audio_file.path)
        audio_transcription.transcription = transcription
        audio_transcription.save()

        return redirect('results')

    return render(request, 'stt_app/record.html')

def upload_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']

        # Save the uploaded audio to the database
        audio_transcription = AudioTranscription()
        audio_transcription.audio_file.save(audio_file.name, audio_file)
        audio_transcription.save()

        # Transcribe the audio
        transcription = transcribe_audio(audio_transcription.audio_file.path)
        audio_transcription.transcription = transcription
        audio_transcription.save()

        return redirect('results')

    return render(request, 'stt_app/upload.html')

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]

def results(request):
    transcriptions = AudioTranscription.objects.all().order_by('-created_at')
    return render(request, 'stt_app/results.html', {'transcriptions': transcriptions})