from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
from RTVC import demo_cli
import random
import asyncio
import time

status_variable = "Null"
Rem_response = ""
Rem_source = ""

pid = "" # participant id
indx = 1 # message index
txt = "" # message text

loop = asyncio.get_event_loop()
def pushremiders(args1):
    global status_variable
    global Rem_source,Rem_response
    print("asyncio process is going on")
    asource = demo_cli.maux(args1[1],indx) ## output text and index
    Rem_response = args1[1]
    Rem_source =  asource  
    time.sleep(args1[0])
    status_variable = "ready"

def process_text(input): 
    try: 
        if 'remind me' in input:
        
            txt = "Okay I'll remind you"
            
            args1 = [0, txt] # arguments in a list. Time and output text 
            
            loop.run_in_executor(None, pushremiders, args1) # default loop's executor async
        
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

@csrf_exempt
def get_response(request):
    response = {'status': None}
    global status_variable
    global Rem_source, Rem_response

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        message = data['message']
        message = message.lower()
        chat_response, audio_source = Chatbot(message)
        response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True, 'audio': audio_source}
        response['status'] = 'ok'
        status_variable = "Null"
        return HttpResponse(json.dumps(response), content_type="application/json")
            
    else:
        response['error'] = 'no post data found'

    return HttpResponse(json.dumps(response), content_type="application/json") 
             

           
            
            

