from django.core.exceptions import ValidationError
from rest_framework.serializers import Serializer,EmailField,DateTimeField,BooleanField,CharField
from Account.models import CustomUser
from Counselor.models import CounselorAppointment
class CounselorPatientAppointmentSerializer(Serializer):
    id=CharField(read_only=True)
    Counselor=EmailField(required=True)
    Patients=EmailField(required=True)
    Appointment=DateTimeField(required=True,allow_null=True)
    AssignedToDoctor=BooleanField(read_only=True,default=False)

    def to_representation(self, instance):
        data=super().to_representation(instance)
        data['AssignedToDoctor']=data.get('AssignedToDoctor')
        counselor_email=data.get('Counselor')
        selected_counselor=CustomUser.objects.filter(email__exact=counselor_email).first()
        CounselorData={}
        CounselorData['first_name']=selected_counselor.first_name
        CounselorData['last_name']=selected_counselor.last_name
        CounselorData['email']=selected_counselor.email
        patient_email=data.get('Patients')
        selected_patients=CustomUser.objects.filter(email__exact=patient_email).first()
        PatientsData={}
        PatientsData['first_name']=selected_patients.first_name
        PatientsData['last_name']=selected_patients.last_name
        PatientsData['email']=selected_patients.email
        data['Counselor']=CounselorData
        data['Patients']=PatientsData
        return data
    def validate(self,data):
        Counslor_email=data.get('Counselor')
        Patient_email=data.get('Patients')
        selected_counselor=CustomUser.objects.filter(email__exact=Counslor_email,role__exact="counselor")
        selected_patients=CustomUser.objects.filter(email__exact=Patient_email,role__exact="patient")
        if (selected_patients.first() is None or selected_counselor.first() is None ):
            raise ValidationError({"Counselor Email or Patient Email is Wrong "})
        self.context['SelectedPatients']=selected_patients
        self.context['SelectedCounselor']=selected_counselor
        return True
    def create(self, validated_data):
        Counselor_email=validated_data.get('Counselor')
        Patient_email=validated_data.get('Patients')
        AssignedToDoctor=validated_data.get('AssignedToDoctor')
        Appointment=validated_data.get('Appointment')

        selected_item = CounselorAppointment.objects.filter(Counselor__email=Counselor_email,
                                                            Patients__email=Patient_email,
                                                            )
        selected_patient=self.context['SelectedPatients'].first()
        selected_counslor=self.context['SelectedCounselor'].first()
        created_item_id=None
        if not AssignedToDoctor:
            created_item = CounselorAppointment.objects.create(
                Counselor_id=selected_counslor.id,
                Patients_id=selected_patient.id,
                Appointment=Appointment
            )
            created_item_id = created_item.id

        selected_item = CounselorAppointment.objects.filter(id=created_item_id)
        return selected_item