from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import sys
sys.path.append("/home/ubuntu/ibas_project")
from lang_detection.text_lang_detect import lang_detect

class LanguageDetectionAPIView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        text = request.data.get('text', '')
        if not text:
            return Response({'error': 'Text is required in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

        detected_language = lang_detect(text)
        return Response({'detected_language': detected_language}, status=status.HTTP_200_OK)
