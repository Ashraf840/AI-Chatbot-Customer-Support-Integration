import speech_recognition as sr
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from datetime import datetime


@csrf_exempt
def transcribe(request):
    # Access the audio file from the request
    print(request)
    files = request.FILES
    file = files.get('files')
    # Save the audio file in webm format
    print(type(file))
    t = datetime.now().strftime("%Y_%m-%I_%M_%S_%p")
    
    # res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    # with open(os.path.abspath(f'{res}.webm'), 'wb') as destination:
    #     for chunk in file.chunks():
    #         destination.write(chunk)

    content_file = ContentFile(file.read())
    file_path = f'./{t}-blob.webm'  # Provide the desired file path
    with open(file_path, 'wb') as file:
        file.write(content_file.read())



    # file.save(os.path.abspath(f'{file.filename}.webm'))
    r = sr.Recognizer()


    webm_file = f'./{t}-blob.webm'
    wav_file = f"./{t}-blob.wav"
    command = ['ffmpeg', '-i', webm_file, wav_file]
    subprocess.run(command, check=True)

    # audio = sr.AudioFile("./blob.wav")
    # print('audio object:',audio)

    # with audio as source:
    #     audio = r.listen(source) 
    #     text = r.recognize_google(audio, language='bn-BD')

    # print(text)




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



    # Return the transcribed text
    # response = jsonify(text)
    # print("Response Data: ", response.data)
    # print("Response Get Data: ", response.get_data)
    # print("Response Get Json: ", response.get_json)
    # print("Response json: ", response.json)
    # print("response: ", dir(response))
    # response.headers.add('Access-Control-Allow-Origin', '*')

    # return response
    # return JsonResponse(text , safe=False)
    return JsonResponse({
        'test': "hi how are you"
    })

