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

txt = "okay" # message text
pid = "U02" # participant id
indx = "M03" # message indexs

loop = asyncio.get_event_loop()
def pushremiders():
    print("asyncio process is going on")
    asource = demo_cli.maux(txt,pid,indx) ## output text, participant id and index

@csrf_exempt
def get_response(request):
    global txt
    global pid
    global indx

    if request.method == 'GET':
        reminders = Reminder.objects.all()
        serializer = ReminderSerializer(reminders, many=True)
        return JsonResponse(serializer.data, safe = False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ReminderSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            pid = data['pid']
            txt = data['txt']
            indx = data['indx']
            loop.run_in_executor(None, pushremiders)
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)
