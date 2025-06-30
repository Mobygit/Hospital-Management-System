from django import forms
from .models import Patient, Doctor, Appointment, Laboratory, Billing,CareerApply,DoctorAppointment

class Patientform(forms.ModelForm):
    class Meta:
        model = Patient 
        fields = '__all__'

class Doctorform(forms.ModelForm):
    class Meta:
        model= Doctor
        fields = '__all__'

class Appointmentform(forms.ModelForm):
    class Meta:
        model = Appointment
        fields ='__all__'

class Laboratoryform(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = '__all__'

class Billingform(forms.ModelForm):
    class Meta:
        model = Billing
        fields ='__all__'

class CareerApplyForm(forms.ModelForm):
    class Meta:
        model = CareerApply
        fields = '__all__'


class DoctorAppointmentForm(forms.ModelForm):
    class meta:
        model = DoctorAppointment
        field = '__all__'
