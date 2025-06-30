from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.
#                  PATIENT DETAILS 
@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'Hospital/patient_list.html', {'patients': patients})

@login_required
def patient_create(request):
    if request.method == 'POST':
        form = Patientform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
        else:
            return render(request, 'Hospital/patient_create.html', {'form': form})
    else:
        form = Patientform()
        return render(request, 'Hospital/patient_create.html', {'form': form})
        


#                DOCTOR DETAILS

@login_required
def doctor_list(request):
    doctors=Doctor.objects.all()
    return render(request, 'Hospital/doctor_list.html', {'doctors': doctors})


@login_required
def doctor_create(request):
    if request.method == 'POST':
        form = Doctorform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
        else:
            return render(request, 'Hospital/doctor_create.html', {'form': form})
    else:
        form = Doctorform()
        return render(request, 'Hospital/doctor_create.html', {'form': form})
    
#                  APPOINTMENT DETAILS

@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'Hospital/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = Appointmentform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
        else:
            return render(request, 'Hospital/appointment_create.html', {'form': form})
    else:
        form = Appointmentform()
        return render(request, 'Hospital/appointment_create.html', {'form': form})
    
#                   LABORATORY DETAILS

# @login_required
# def laboratory_list(request):
#     results = Laboratory.objects.select_related('patient').all()
#     return render(request, 'Hospital/laboratory_list.html', {'results': results})

# @login_required
# def laboratory_create(request):
#     if request.method == 'POST':
#         form = Laboratoryform(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('laboratory_list')
#         else:
#             return render(request, 'Hospital/laboratory_create.html', {'form': form})
#     else:
#         form = Laboratoryform()
#         return render(request, 'Hospital/laboratory_create.html', {'form': form})
    

# @login_required
from django.shortcuts import render
from django.contrib import messages
from .models import Patient, Laboratory, LabTest
from datetime import date
from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient, Laboratory, LabTest

def lab_appointment(request):
    lab_status = None

    if request.method == 'POST':
        if 'lab_test' in request.POST:
            full_name = request.POST.get('patient_name')
            age = request.POST.get('patient_age')  # get age instead of dob
            mobile = request.POST.get('contact_phone')
            email = request.POST.get('email')
            test = request.POST.get('lab_test')
            appointment_date = request.POST.get('appointment_date')

            # Convert age to date_of_birth assuming birthday already happened this year
            if age and age.isdigit():
                age = int(age)
                today = date.today()
                dob_year = today.year - age
                dob = date(dob_year, today.month, today.day)
            else:
                dob = None  # handle invalid age or missing age gracefully

            # Split full name into first and last name
            name_parts = full_name.strip().split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            # Create or get patient by Contact_number
            patient, created = Patient.objects.get_or_create(
                Contact_number=mobile,
                defaults={
                    'First_name': first_name,
                    'Last_name': last_name,
                    'Date_of_birth': dob,
                    'Email': email,
                }
            )

            # Create lab appointment
            lab_entry = Laboratory.objects.create(
                patient=patient,
                appointment_date=appointment_date,
                mobile=mobile,
            )

            lab_test_obj = LabTest.objects.filter(name__iexact=test).first()
            if lab_test_obj:
                lab_entry.tests.add(lab_test_obj)
                messages.success(request, "Lab appointment booked successfully!")
            else:
                messages.warning(request, "Selected test not found.")

            return redirect('lab_appointment')

        elif 'mobile_number' in request.POST:
            mobile = request.POST.get('mobile_number', '').strip()
            lab_status = Laboratory.objects.filter(mobile__iexact=mobile).order_by('-appointment_date').first()
            if not lab_status:
                messages.error(request, "No lab result found for this mobile number.")

            # try:
            #     lab_status = Laboratory.objects.filter(mobile__iexact=mobile).order_by('-appointment_date').first()
            #     if not lab_status:
            #         messages.error(request, "No lab result found for this mobile number.")

            #     lab_status = Laboratory.objects.filter(mobile__iexact=mobile).latest('appointment_date')
            # except Laboratory.DoesNotExist:
            #     messages.error(request, "No lab result found for this mobile number.")

    return render(request, 'Hospital/mubi/lab_appointment.html', {'lab_status': lab_status})

    #     elif 'mobile_number' in request.POST:
    #         mobile = request.POST.get('mobile_number')
    #         try:
    #             lab_status = Laboratory.objects.filter(mobile=mobile).latest('appointment_date')
    #         except Laboratory.DoesNotExist:
    #             messages.error(request, "No lab result found for this mobile number.")

    # return render(request, 'Hospital/mubi/lab_appointment.html', {'lab_status': lab_status})

from django.http import FileResponse, Http404

def download_lab_report(request, lab_id):
    try:
        lab = Laboratory.objects.get(id=lab_id)
        if lab.report_file:
            return FileResponse(lab.report_file.open('rb'), as_attachment=True, filename=lab.report_file.name)
        else:
            messages.error(request, "Report file not available yet.")
            return redirect('lab_appointment')
    except Laboratory.DoesNotExist:
        raise Http404("Lab appointment not found.")




    

#                     BILLING DETAILS

@login_required
def billing_list(request):
    bills = Billing.objects.select_related('patient').all()
    return render(request, 'Hospital/billing_list.html', {'bills': bills})


@login_required
def billing_create(request):
    if request.method == 'POST':
        form = Billingform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('billing_list')
        else:
            return render(request, 'Hospital/billing_create.html', {'form': form})
    else:
        form = Billingform()
        return render(request, 'Hospital/billing_create.html', {'form': form})
    
 
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import CareerApplyForm

# @login_required
from django.http import JsonResponse

def career_apply(request):
    if request.method == 'POST':
        form = CareerApplyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Uploaded successfully! We will contact you if eligible.'})
            return render(request, 'Hospital/mubi/career.html', {
                'form': CareerApplyForm(),
                'success_message': 'Uploaded successfully! We will contact you if eligible.'
            })
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            return render(request, 'Hospital/mubi/career.html', {'form': form})
    else:
        form = CareerApplyForm()
        return render(request, 'Hospital/mubi/career.html', {'form': form})



    
def index(request):
    return render(request, 'Hospital/mubi/index.html')



# def lab_appointment(request):
#     return render(request, 'Hospital/mubi/lab_appointment.html')

def doctors(request):
    return render(request, 'Hospital/mubi/doctors.html')

def departments(request):
    return render(request, 'Hospital/mubi/departments.html')

def contact(request):
    return render(request, 'Hospital/mubi/contact.html')

def career(request):
    return render(request, 'Hospital/mubi/career.html')

def founder(request):
    return render(request, 'Hospital/mubi/founder.html')

def doctor_appointment(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        patient_age = request.POST.get('patient_age')
        contact_phone = request.POST.get('contact_phone')
        email = request.POST.get('email')
        doctor = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')

        # Save the appointment
        DoctorAppointment.objects.create(
            patient_name=patient_name,
            patient_age=patient_age,
            contact_phone=contact_phone,
            email=email,
            doctor=doctor,
            appointment_date=appointment_date
        )
        messages.success(request, 'Your appointment has been booked successfully!')
        return redirect('doctor_appointment')  # Reload same page after submission

    return render(request, 'Hospital/mubi/doctor_appointment.html')