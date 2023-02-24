from django.contrib import admin
from .models import CounselorAppointment
class CounselorAdmin(admin.ModelAdmin):
    list_display = ('Counselor','Patients')

admin.site.register(CounselorAppointment,CounselorAdmin)
# Register your models here.
