from django.contrib import admin
from .models import CounselorAppointment,ModelFormCounselorAppointment
class CounselorAdmin(admin.ModelAdmin):
    form = ModelFormCounselorAppointment
    list_display = ('Counselor','Patient')

admin.site.register(CounselorAppointment,CounselorAdmin)
# Register your models here.
