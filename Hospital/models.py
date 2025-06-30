from django.db import models

class Patient(models.Model):
    First_name = models.CharField(max_length=100)
    Last_name = models.CharField(max_length=100)
    Date_of_birth = models.DateField()
    Contact_number = models.CharField(max_length=15)
    Email = models.EmailField()
    Address = models.TextField()

    def __str__(self):
        return f"{self.First_name} {self.Last_name}"

class Doctor(models.Model):
    First_name = models.CharField(max_length=100)
    Last_name = models.CharField(max_length=100)
    Specialization = models.CharField(max_length=100)
    Email = models.EmailField()
    Contact_number = models.CharField(max_length=15)
    Availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.First_name} {self.Last_name} ({self.Specialization})"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('Scheduled', 'Scheduled'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled')
        ],
        default='Scheduled'
    )

    def __str__(self):
        return f"Appointment: {self.patient} with Dr. {self.doctor} on {self.appointment_date}"

class LabTest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class Laboratory(models.Model):
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     tests = models.ManyToManyField(LabTest)
#     appointment_date = models.DateField()
#     result = models.TextField(blank=True, null=True)
#     report_file = models.FileField(upload_to='lab_reports/', blank=True, null=True)

#     def __str__(self):
#         return f"Lab appointment for {self.patient} on {self.appointment_date}"

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('In Progress', 'In Progress'),
    ('Done', 'Done'),
]



class Laboratory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    tests = models.ManyToManyField(LabTest)
    appointment_date = models.DateField()
    result = models.TextField(blank=True, null=True)
    report_file = models.FileField(upload_to='lab_reports/', blank=True, null=True)

    # 🔽 Add this field
    mobile = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Lab appointment for {self.patient} on {self.appointment_date}"


class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_issued = models.DateField()
    service_description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bill for {self.patient} on {self.date_issued} - Rs. {self.amount}"

# career apply

class CareerApply(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)  # add if needed
    email = models.EmailField(null=True, blank=True)  # allow null and blank
    phone = models.CharField(max_length=20, null=True, blank=True)  # similarly for phone
    role = models.CharField(max_length=100)
    cv_file = models.FileField(upload_to='cvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application for {self.role} on {self.uploaded_at.strftime('%Y-%m-%d')}"


    



class DoctorAppointment(models.Model):
    DOCTOR_CHOICES = [
        ('ethel_davis', 'Dr. Ethel Davis'),
        ('dand_mories', 'Dr. Dand Mories'),
        ('dr_lee', 'Dr. Align Board'),
    ]

    patient_name = models.CharField(max_length=100)
    patient_age = models.PositiveIntegerField()
    contact_phone = models.CharField(max_length=15)
    email = models.EmailField()
    doctor = models.CharField(max_length=50, choices=DOCTOR_CHOICES)
    appointment_date = models.CharField(max_length=100)  # Use `models.DateTimeField()` if datetime format is guaranteed

    def __str__(self):
        return f"{self.patient_name} - {self.doctor} on {self.appointment_date}"
