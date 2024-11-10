# hospital/urls.py
from django.urls import path
from .views import book_appointment_view, view_appointments_view, patient_list
from . import views
urlpatterns = [
    #for homepage
    path('', views.homepage, name='homepage' ), 

    # For about us 
    path('aboutus', views.aboutus, name='aboutus'),

    # fro Creating new Patient record 

    path('patient/create/', views.create_patient, name='create_patient' ),
    path('patients/', views.patient_list, name='patient_list' ),
    path('patient/detail/<int:product_id>/', views.patient_detail, name='patient_detail'),
    path('patient/delete/<int:patient_id>/', views.patient_delete, name='patient_delete'),

    path('patient/update/<int:product_id>/', views.update_patient, name='patient_update'),


    # For appointments 
    path('appointment/delete/<int:appointment_id>/', views.delete_appointment_view, name='appointment_delete'),
    path('patient/<int:patient_id>/book/', book_appointment_view, name='book_appointment'),
    path('appointments/', view_appointments_view, name='view_appointments'),

    # For the products
    path('product/list/', views.product_list, name='product_list'),
    path('product/create/', views.create_product, name='create_product'),
    path('product/detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('product/update/<int:product_id>/', views.update_product, name='product_update'),

    #For the doctors
    path('doctors/', views.sorted_doctor_list, name='doctor_list'),
    path('doctor/create', views.create_doctor, name='create_doctor'),
    path('doctor/delete/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),

         

    #For the workers
    path('workers/', views.sorted_workers_list, name='worker_list'),
    path('worker/create', views.create_worker, name='create_worker'),
    path('worker/delete/<int:worker_id>/', views.delete_worker, name='delete_worker'),
    # For the shortest path algorithms
    path('shortest-path/', views.shortest_path_view, name='shortest_path')
]
