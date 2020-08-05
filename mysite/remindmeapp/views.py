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

str pid = "" # participant id
int indx = 0 # message index
str txt = "" # message text

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
    print("printing argument to push")
    print(args1[1])
    print(asource)


def process_text(input): 
    try: 
        if 'remind me' in input:
        
            chat_response= "Okay I'll remind you buddy"
            
            args1 = [0, txt] # arguments in a list. Time and output text 
            
            loop.run_in_executor(None, pushremiders, args1) # default loop's executor async
        
            return chat_response, "hello"
        
        else:
            
            return "Say that again?", "hello"

    except :
        
        return "Invalid Conversation", "hello"


def Chatbot(text):
    chatresponse, audio_source = process_text(text)
    return chatresponse, audio_source

def home(request, template_name="home.html"):
    context = {'title': 'KIN'} ## passes context to template home.html
    return render(request, template_name, context) ## allow rendering of the home page

@csrf_exempt
def get_response(request):
    response = {'status': None}
    global status_variable
    global Rem_source,Rem_response

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        message = data['message']
        print("frontend fetch reminder response")
        print(message)
        message=message.lower()
        #m1=data[]
        #print("this is message.reminded")
        #print(message.reminded)
        if status_variable=="ready" and message == "remindercheck_false":
    
            chat_response=Rem_response
            audio_source=Rem_source
            #chat_response="reminderminder"
            #audio_source = "hello"
            
            print("Printing Ready reminder variables inside post request :")
            print(chat_response)
            print(audio_source)

            response['message'] = {'reminder': True,'text': chat_response, 'user': False, 'chat_bot': True, 'audio': audio_source}
            response['status'] = 'ok'

        elif message == "remindercheck_true":
            chat_response="backend reminded"
            audio_source="hello"
            response['message'] = {'reminder': False,'text': chat_response, 'user': False, 'chat_bot': True, 'audio': audio_source}
            response['status'] = 'ok'
            status_variable = "Null"
                        
        elif message != "remindercheck_false":
            #data = json.loads(request.body.decode('utf-8'))
            #message = data['message'] # string message from user
            #print(message)
            print("normal chat request")
            chat_response,audio_source=Chatbot(message)
            #chat_response="hello THERE"
            #audio_source = demo_cli.maux(chat_response,176)
            #audio_source = "demo_output_1651651"
            print(chat_response)
            print(audio_source)
            response['message'] = {'reminder': False,'text': chat_response, 'user': False, 'chat_bot': True, 'audio': audio_source}
            response['status'] = 'ok'
            status_variable = "Null"
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            response['error'] = 'no post data found'
            

    else:
        response['error'] = 'no post data found'

    return HttpResponse(json.dumps(response), content_type="application/json") 
             

           
            
            

