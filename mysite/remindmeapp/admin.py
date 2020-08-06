from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Reminder

#admin.site.register(Reminder)

@admin.register(Reminder)
class ReminderAdmin(ImportExportModelAdmin):
	pass