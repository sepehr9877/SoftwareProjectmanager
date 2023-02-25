from django.core.exceptions import ValidationError
from rest_framework.serializers import Serializer,EmailField,DateTimeField,BooleanField,CharField
from Account.models import CustomUser
from Counselor.models import CounselorAppointment
from Questions.models import SelfAssessment
class CounselorPatientAppointmentSerializer(Serializer):
    id=CharField(read_only=True)
    Counselor=EmailField(required=False)
    Patients=EmailField(required=True)
    Appointment=DateTimeField(required=True,allow_null=True)
    AssignedToDoctor=BooleanField(read_only=True,default=False)
    def to_representation(self, instance):
        data=super().to_representation(instance)
        request_data=self.context['data']
        counselor_email = self.context['authuser'].first().email
        selected_counselor=CustomUser.objects.filter(email__exact=counselor_email).first()
        CounselorData={}
        CounselorData['first_name']=selected_counselor.first_name
        CounselorData['last_name']=selected_counselor.last_name
        CounselorData['email']=selected_counselor.email
        patient_email=request_data.get('Patients')
        if  patient_email :
            selected_patients=CounselorAppointment.objects.filter(Counselor_id=selected_counselor.id,Patients__email=patient_email).all()
        else:
            selected_patients=CounselorAppointment.objects.filter(Counselor_id=selected_counselor.id).all()
        PatientList=[]
        selected_patients_len=selected_patients.count()
        PatientsData={}
        Result=[]
        if selected_patients_len>1:

            for patients in selected_patients:
                patient=patients.first()
                PatientsData={}
                PatientsData['first_name'] = patient.Patients.first_name
                PatientsData['last_name'] = patient.Patients.last_name
                PatientsData['email'] = patient.Patients.email
                data['Appointment']=patient.Appointment
                PatientList.append(PatientsData)
        elif selected_patients:
            selected_patients=selected_patients.first()
            PatientsData['first_name'] = selected_patients.Patients.first_name
            PatientsData['last_name'] = selected_patients.Patients.last_name
            PatientsData['email'] = selected_patients.Patients.email
            data['Appointment'] = selected_patients.Appointment
            PatientList.append(PatientsData)
        else:
            data['Appointment']=None

        data['Counselor']=CounselorData
        data['Patients']=PatientList
        Result.append(data)
        return data
    def validate(self,data):
        CounselorAuth=self.context['authuser'].first()
        Patient_email=data.get('Patients')
        selected_counselor=CustomUser.objects.filter(email__exact=CounselorAuth.email,role__exact="counselor")
        selected_patients=CustomUser.objects.filter(email__exact=Patient_email,role__exact="patient")
        if (selected_patients.first() is None or selected_counselor.first() is None ):
            raise ValidationError({"Counselor Email or Patient Email is Wrong "})
        self.context['SelectedPatients']=selected_patients
        self.context['SelectedCounselor']=selected_counselor
        return True
    def update(self, counselor, validated_data):
        Counselor_email=self.context['authuser'].first()
        Patient_email=validated_data.get('Patients')
        AssignedToDoctor=validated_data.get('AssignedToDoctor')
        Appointment=validated_data.get('Appointment')
        selected_item = CounselorAppointment.objects.filter(
                                                            Patients__email=Patient_email,
                                                            )
        selected_patient=self.context['SelectedPatients'].first()
        selected_counslor=self.context['SelectedCounselor'].first()
        created_item_id=None
        if (AssignedToDoctor is None) and ((selected_item.first().Counselor==selected_counslor)or (selected_item.first().Counselor is None)):
            created_item = CounselorAppointment.objects.update(
                Counselor_id=selected_counslor.id,
                Patients_id=selected_patient.id,
                Appointment=Appointment
            )
            selected_appointment=CounselorAppointment.objects.filter(
                Counselor_id=selected_counslor.id,Patients_id=selected_patient.id,Appointment=Appointment
            ).first()
            created_item_id = selected_appointment.id

        selected_item = CounselorAppointment.objects.filter(id=created_item_id)
        return selected_item