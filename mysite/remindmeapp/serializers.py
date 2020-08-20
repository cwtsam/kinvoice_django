
from rest_framework import serializers
from .models import Reminder, Logger

class ReminderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reminder
		fields = '__all__'


class LoggerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Logger
		fields = '__all__'