from django.contrib import admin

# Register your models here.
from .models import Reminder

admin.site.register(Reminder)