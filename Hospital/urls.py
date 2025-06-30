from django.urls import path
from . import views 

urlpatterns = [
    # path('patients/',views.patient_list, name='patient_list'),
    # path('patient/new/', views.patient_create, name='patient_create'),
    # path('doctors/', views.doctor_list, name='doctor_list'),
    # path('doctors/new/', views.doctor_create, name='doctor_create'),
    # path('appointments/', views.appointment_list, name='appointment_list'),
    # path('appointment/new/', views.appointment_create, name='appointment_create'),
    # path('lab/', views.laboratory_list, name='laboratory_list'),
    # path('lab/new/', views.laboratory_create, name='laboratory_create'),
    # path('bill/', views.billing_list, name='billing_list'),
    # path('bill/new/', views.billing_create, name='billing_create'),
    # path('career/', views.career_apply, name='career_apply')
    path('',views.index, name='index'),
    path('lab_appointment/',views.lab_appointment, name='lab_appointment'),
    path('doctors/',views.doctors, name='doctors'),
    path('departments/',views.departments, name='departments'),
    path('contact/',views.contact, name='contact'),
    path('career/',views.career_apply, name='career'),
    path('founder/',views.founder, name='founder'),
    path('doctor_appointment',views.doctor_appointment, name='doctor_appointment'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    
]