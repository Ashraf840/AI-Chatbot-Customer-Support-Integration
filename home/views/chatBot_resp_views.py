from django.http import HttpResponse, JsonResponse
import json
from chat import get_response
from ..models import ChatbotVisitorMessage
from ..utils.get_ip import get_client_ip


def bot_resp(request):
    if request.method == "POST":
        # msg = f"'bot_resp' func is called!"
        msg = json.load(request)['message'] #Get data from POST request
        # TODO: Check if the msg has valid text
        # TODO: Get the current date/time
        # TODO: Store bot-visitors convo
        response = get_response(msg)
        # print("#"*50)
        # print('User:', request.user)
        # print('Client IP:', get_client_ip(request))
        # count = 0
        # request.session[f'{get_client_ip(request)}'] = {
        #         "client_ip": get_client_ip(request),
        # }
        # if response == "I do not understand...":
            # print(request.session[get_client_ip(request)])
            # # print(request.session[get_client_ip(request)]['client_ip'])
            # if request.session[get_client_ip(request)]['client_ip'] == get_client_ip(request):
            #     request.session[get_client_ip(request)]['count'] += 1
            #     print(request.session[get_client_ip(request)]['count'])
            # # request.session['count'] = 0
            # request.session['count'] += 1
            # # count = request.session['count']
            # print('session count:', request.session['count'])
            # # count += 1
            # # print('count:', count)
            # if request.session['count'] > 5:
            #     request.session['count'] = 0
            #     response = "Would you like to talk to out customer support?"
                # data = { 'answer': f'{response}' }
                # return JsonResponse(data)
        visitor_ip = get_client_ip(request)
        # now = datetime.now()
        print(f"visitor ip: {visitor_ip}")
        # print(f"visitor msg: {msg}")
        # print(f"response: {response}")
        # print(f"msg time: {now}")
        # print("#"*50)
        
        # Store chatbot-visitor message
        ChatbotVisitorMessage.objects.create(
            client_ip=visitor_ip,
            visitors_msg=msg,
            bot_msg=response
        )
        data = { 'answer': f'{response}' }
        return JsonResponse(data)
    return HttpResponse('No content!', content_type='text/plain')
