import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from googletrans import Translator
from gtts import gTTS
import asyncio

async def translate_text_multiple(text: str, target_languages: list) -> dict:
    translator = Translator()
    translations = {}

    for lang in target_languages:
        try:
            translated_text = await translator.translate(text, dest=lang)
            translations[lang] = translated_text.text
        except Exception as e:
            print(f"Error translating to {lang}: {e}")
            translations[lang] = ""

    return translations

async def translate(request):
    if request.method == 'POST':
        text_to_translate = request.POST.get('text', '')
        language_codes_str = request.POST.get('languages', '')
        target_languages = [lang.strip() for lang in language_codes_str.split(',') if lang.strip()]

        if not target_languages:
            return JsonResponse({'error': 'No valid target languages provided.'}, status=400)

        translations = await translate_text_multiple(text_to_translate, target_languages)

        # Save translations to a file
        with open("translations.txt", "w", encoding="utf-8") as file:
            file.write(f"Original Text: {text_to_translate}\n\n")
            for lang, translated_text in translations.items():
                file.write(f"{lang}: {translated_text}\n")

        # Generate .mp3 files for each translation
        mp3_files = {}
        for lang, translated_text in translations.items():
            if translated_text:  # Only generate if translation is not empty
                tts = gTTS(translated_text, lang=lang)  # Use the target language for TTS
                mp3_file_name = f"translation_{lang}.mp3"
                mp3_file_path = os.path.join(settings.MEDIA_ROOT, mp3_file_name)

                # Ensure the media directory exists
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

                tts.save(mp3_file_path)
                mp3_files[lang] = os.path.join(settings.MEDIA_URL, mp3_file_name)

        return JsonResponse({
            'translations': translations,
            'mp3_files': mp3_files  # Return paths to the generated .mp3 files
        })

    return render(request, 'translator/translate.html')