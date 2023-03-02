
from rest_framework.serializers import Serializer,CharField,BooleanField
from Questions.models import SelfAssessment
from Counselor.models import CounselorAppointment
class SelfAssessMentSerializer(Serializer):
    # Patient = CharField(required=True)
    Question1 = BooleanField(required=True)
    Question2 = BooleanField(required=True)
    Question3 = BooleanField(required=True)
    Question4 = BooleanField(required=True)
    Question5 = BooleanField(required=True)
    Question6 = BooleanField(required=True)
    Question7 = BooleanField(required=True)
    Question8=BooleanField(required=True)
    Question9=BooleanField(required=True)
    def create(self, validated_data):
        q1=validated_data.get('Question1')
        q2=validated_data.get('Question2')
        q3=validated_data.get('Question3')
        q4=validated_data.get('Question4')
        q5=validated_data.get('Question5')
        q6=validated_data.get('Question6')
        q7=validated_data.get('Question7')
        q8=validated_data.get('Question8')
        q9=validated_data.get('Question9')

        patient=self.context['patient'].first()
        selected_selfassessment=SelfAssessment.objects.filter(Patient_id=patient.id).first()
        if selected_selfassessment is None:
            selected_selfassessment=SelfAssessment.objects.create(
                Patient_id=patient.id,
                Question1=q1,
                Question2=q2,Question3=q3,Question4=q4,Question5=q5,
                Question6=q6,Question7=q7,Question8=q8,Question9=q9

            )
        selected_counselor_appointment=CounselorAppointment.objects.filter(Patients_id=selected_selfassessment.Patient.id).first()
        if selected_counselor_appointment is None:
            selected_counselor_appointment=CounselorAppointment.objects.create(
                Patients_id=selected_selfassessment.Patient.id
            )
        return selected_counselor_appointment