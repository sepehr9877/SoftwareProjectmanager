from django.contrib import admin
from .models import DoctorAppointment,ModelFormDoctorAppointment
# Register your models here.
class DoctorAppointmentAdmin(admin.ModelAdmin):
    form = ModelFormDoctorAppointment
    list_display = ('Doctor','Patient','Appointment')

admin.site.register(DoctorAppointment,DoctorAppointmentAdmin)