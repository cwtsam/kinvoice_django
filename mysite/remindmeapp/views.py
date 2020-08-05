from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .serializers import ReminderSerializer
from .models import Reminder

import json
from RTVC import demo_cli
import random
import asyncio
import time

txt = "okay I'll remind you" # message text
pid = "U02" # participant id
indx = "M_1" # message indexs

loop = asyncio.get_event_loop()
def pushremiders():
    print("asyncio process is going on")
    asource = demo_cli.maux(txt,pid,indx) ## output text, participant id and index

@csrf_exempt
def get_response(request):
    response = {'status': None}
    global status_variable
    global Rem_source, Rem_response

    if request.method == 'GET':
        reminders = Reminder.objects.all()
        serializer = ReminderSerializer(reminders, many=True)
        return JsonResponse(serializer.data, safe = False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ReminderSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            loop.run_in_executor(None, pushremiders) # activates async function to generate audio file
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

    '''    
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        message = data['message']
        message = message.lower()
        chat_response, audio_source = Chatbot(message)
        response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True, 'audio': audio_source}
        response['status'] = 'ok'
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response['error'] = 'no post data found'

    return HttpResponse(json.dumps(response), content_type="application/json") 
    '''

'''  
def process_text(input): 
    try: 
        if 'remind me' in input:
            args1 = [0, txt] # arguments in a list. Time and output text 
            loop.run_in_executor(None, pushremiders) # default loop's executor async
            return txt, "hello"
        else:
            return "Say that again?", "hello"
    except :
        return "Invalid Conversation", "hello"


def Chatbot(text):
    chatresponse, audio_source = process_text(text)
    return chatresponse, audio_source


def home(request, template_name="home.html"): ## 'root' directory
    context = {'title': 'KIN'} ## passes context to template home.html
    return render(request, template_name, context) ## allow rendering of the home page

class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all().order_by('pid')
    serializer_class = ReminderSerializer

            
class ReminderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        reminders = Reminder.objects.all()
        serializer = ReminderSerializer(reminders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReminderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
#@permission_classes([IsAuthenticated])
def reminder_list(request):
    
    if request.method == 'GET':
        reminders = Reminder.objects.all()
        serializer = ReminderSerializer(reminders, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ReminderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''