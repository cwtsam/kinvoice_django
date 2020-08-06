from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .serializers import ReminderSerializer
from .models import Reminder

from RTVC import demo_cli
import asyncio
import boto3
from botocore.exceptions import NoCredentialsError

txt = "okay" # message text
pid = "U02" # participant id
indx = "M03" # message indexs

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

loop = asyncio.get_event_loop()
def generate_store():
    print("asyncio process is going on")
    asource = demo_cli.maux(txt,pid,indx) ## output text, participant id and index
    #uploaded = upload_to_aws(asource, 'djangomediakinvoice', 'test_upload.mp3') # uploading to aws s3 bucket

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
            loop.run_in_executor(None, generate_store) # generate audio files asynchroniously
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

