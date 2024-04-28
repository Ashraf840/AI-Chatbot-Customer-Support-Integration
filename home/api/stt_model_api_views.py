import speech_recognition as sr
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from datetime import datetime
# from speechbrain.pretrained import EncoderClassifier

@csrf_exempt
def transcribe(request):
    # Access the audio file from the request
    files = request.FILES
    file = files.get('files')
    # Save the audio file in webm format
    t = datetime.now().strftime("%Y_%m-%I_%M_%S_%p")

    content_file = ContentFile(file.read())
    file_path = f'./{t}-blob.webm'  # Provide the desired file path
    with open(file_path, 'wb') as file:
        file.write(content_file.read())

    webm_file = f'./{t}-blob.webm'   # predefined filename; make search easy to convert into wav format
    wav_file = f"./{t}-blob.wav"     # defined wav-format filename
    command = ['ffmpeg', '-i', webm_file, wav_file]     # actual webm-wav conversion
    subprocess.run(command, check=True)

    # Transcribe the audio
    r = sr.Recognizer()
    audio = sr.AudioFile(f"./{t}-blob.wav")
    text = ""
    try:
        with audio as source:
            audio = r.listen(source) 
            text = r.recognize_google(audio, language='bn-BD')
    except sr.UnknownValueError:
        text = "Speech could not be recognized"
    except sr.RequestError as e:
        text = "Error occurred during speech recognition: {0}".format(e)

    # Return the transcribed text
    return JsonResponse({'transcription': text}, safe= False)




# @csrf_exempt
# def transcribe(request):
#     files = request.FILES
#     file = files.get('files')

#     t = datetime.now().strftime("%Y_%m-%I_%M_%S_%p")

#     content_file = ContentFile(file.read())
#     file_path = f'./{t}-blob.webm'  # Provide the desired file path
#     with open(file_path, 'wb') as file:
#         file.write(content_file.read())

#     r = sr.Recognizer()

#     webm_file = f'./{t}-blob.webm'
#     wav_file = f"./{t}-blob.wav"
#     command = ['ffmpeg', '-i', webm_file, wav_file]
#     subprocess.run(command, check=True)

#     # Transcribe the audio
#     r = sr.Recognizer()
#     audio = sr.AudioFile(f"./{t}-blob.wav")
#     text = ""
#     try:
#         with audio as source:
#             audio_data = r.record(source)
#             if detect_language(wav_file) == "bn":    
#                 language_code = 'bn-BD'
#                 print("language: ", language_code)
#             else: 
#                 language_code = 'en'
#             recognized = r.recognize_google(audio_data, language=language_code, show_all=True)
#             print("Recognized: ", recognized)
            
#             alternatives = recognized.get('alternative', [])
#             if alternatives:
#                 text = alternatives[0]['transcript']
#                 confidence = alternatives[0]['confidence']
#             else:
#                 text = "No speech recognized"
#                 confidence = 0.0

#     except sr.UnknownValueError:
#         text = "Speech could not be recognized"
#         confidence = 0.0
#     except sr.RequestError as e:
#         text = "Error occurred during speech recognition: {0}".format(e)
#         confidence = 0.0

#     # Return the transcribed text and confidence level
#     return JsonResponse({'transcription': text, 'confidence': confidence}, safe=False)


# def detect_language(file_path):
#     # Use language detection library or API to detect the language of the audio
#     language_id = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")
    
#     preprocessed = language_id.load_audio(file_path)
#     prediction =  language_id.classify_batch(preprocessed)
    
#     language_code = prediction[3]

#     language_name = language_code[0].split(":")[1].strip()
#     print("language_name:", language_name)

#     if language_name == 'Bengali':
#         return 'bn'
#     else:
#         return 'en'


