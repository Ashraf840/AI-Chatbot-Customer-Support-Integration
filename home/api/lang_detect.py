from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
import os
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import sys
sys.path.append("/home/ubuntu/ibas_project")
from lang_detection.text_lang_detect import lang_detect

@csrf_exempt
def lang_detector(request):
    if request.method == 'POST':
        record = json.loads(request.body)
        text = record['text']
        detected_language = lang_detect(text)
        # detected_language = lang_detect_logic(text)
        # print(detected_language)
        print(text)
        print(detected_language)

        return JsonResponse({'detected_language': detected_language}, status=201)
    return JsonResponse({'message': 'Invalid request'}, status=400)
