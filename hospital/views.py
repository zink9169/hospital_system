# hospital/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Appointment, Product, Doctor, Location, Worker
from .queue import AppointmentQueue
from datetime import datetime
from .utils import quick_sort_doctors, merge_sort_workers
from .utils import dijkstra_shortest_path
from .forms import ShortestPathForm
from django.contrib import messages
# Create a global instance of the queue (for demonstration purposes)
appointment_queue = AppointmentQueue()



# For patient record
def patient_list(request):
    patients = Patient.objects.all().order_by('-id')
    return render(request, 'patientList.html', {'patients': patients})
#For creating patient record 

def create_patient(request):
    if request.method == "GET":
        return render(request, 'create_patient.html')

    if request.method == "POST":
        try:
            # Create the patient record with data from the form
            Patient.objects.create(
                patient_id=int(request.POST.get('patient_id')),
                name=request.POST.get('name'),
                age=int(request.POST.get('age')),
                address=request.POST.get('address')
            )
            # Redirect to the patient list view after creation
            messages.error(request, 'Please remember your patient id for booking appointment!')
            return redirect('patient_list')
        except ValueError:
            # Handle invalid input (like non-integer age or patient_id)
            return render(request, 'create_patient.html', {
                'error': 'Invalid data provided. Please check the inputs.'
            })

def patient_detail(request, patient_id):
    # Get the product based on the ID or return a 404 if not found
    patients = get_object_or_404(Patient, id=patient_id)
    return render(request, 'patientDetail.html', {'products': patients})



def patient_delete(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return redirect('patient_list')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient

def update_patient(request, patient_id):
    # Retrieve the existing patient instance
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "GET":
        # Render the form with the existing patient data
        return render(request, 'create_Patient.html', {'patient': patient})

    elif request.method == "POST":
        # Update the patient's fields with data from the form
        patient.name = request.POST.get('name')
        patient.age = request.POST.get('age')
        patient.address = request.POST.get('address')
        patient.save()  # Save the updated instance to the database
        
        return redirect('patient_list')  # Use the named URL pattern for redirection

    return redirect('patient_list')  # Fallback redirect for other request types



# For appointment
def book_appointment_view(request, patient_id): 
    patient = get_object_or_404(Patient, pk=patient_id)

    if request.method == "POST":
        appointment_date_str = request.POST.get('appointment_date')

        # Validate that the appointment date string is not empty
        if not appointment_date_str:
            messages.error(request, 'Please provide a valid appointment date.')
            return render(request, 'book_appointment.html', {'patient': patient})

        try:
            # Parse the appointment date from the string
            appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%dT%H:%M')

            # Create the appointment
            appointment = Appointment.objects.create(patient=patient, appointment_date=appointment_date)

            # Assuming appointment_queue is a valid instance for managing appointments
            appointment_queue.add_appointment(appointment)

            messages.success(request, 'Appointment booked successfully!')
            return redirect('homepage')  # Redirect to the homepage

        except ValueError:
            messages.error(request, 'Invalid date format. Please use the correct format.')
            return render(request, 'book_appointment.html', {'patient': patient})

    return render(request, 'book_appointment.html', {'patient': patient})

def view_appointments_view(request):
    appointments = Appointment.objects.order_by('id')
    return render(request, 'view_appointments.html', {'appointments': appointments})

def delete_appointment_view(request, appointment_id):
    # Fetch the appointment or return a 404 error if not found
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if the request method is POST to ensure it's a deletion request
    if request.method == "POST":
        appointment.delete()  # Delete the appointment
        messages.success(request, 'Appointment deleted successfully.')  # Success message
        return redirect('view_appointments')  # Redirect to the appointment list view

    # If the request method is not POST, redirect to the appointment list
    return redirect('view_appointments')

#For Homepage 
def homepage(request):

    return render(request, 'homePage.html' )

# For About 
def aboutus(request):

    return render(request, 'aboutus.html')

# For product

def product_list(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'productList.html', {'products': products})

def create_product(request):
    if request.method == "GET":
        return render(request, 'createProduct.html')
    
    if request.method == "POST":
        # Accessing the data from request.POST
        patient = Product.objects.create(
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            description=request.POST.get('description'),
            category=request.POST.get('category'),
        )
        # No need to call save() again since create() already saves the instance
        return redirect('../list/')  # Use the named URL pattern for the patient list

    return redirect('../list/')  # Fallback redirect for non-POST requests

def update_product(request, product_id):
    # Retrieve the product by ID or return 404 if it doesn't exist
    product = get_object_or_404(Product, id=product_id)

    if request.method == "GET":
        # Render the form with the existing product data
        return render(request, 'createProduct.html', {'product': product})

    elif request.method == "POST":
        # Update the product fields with data from the form
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.category = request.POST.get('category')
        product.save()  # Save the updated instance to the database
        
        return redirect('product_list')  # Use the named URL pattern for redirection

    return redirect('product_list')  # Fallback redirect for other request types

def product_detail(request, product_id):
    # Get the product based on the ID or return a 404 if not found
    products = get_object_or_404(Product, id=product_id)
    return render(request, 'productDetail.html', {'products': products})

def product_delete(request, product_id):
    products = Product.objects.filter(id = product_id)
    products.delete()
    return redirect('../../list/')
    

# For Quick sort doctor

def sorted_doctor_list(request):
    doctors = list(Doctor.objects.all())  # Convert queryset to a list for sorting
    sorted_doctors = quick_sort_doctors(doctors, key=lambda x: x.years_of_experience)  # Sort by experience
    context = {'doctors': sorted_doctors}
    return render(request, 'quick_sort_doctor_list.html', context)

def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    return redirect('doctor_list')

def create_doctor(request):
    if request.method == "GET":
        return render(request, 'createDoctor.html')
    
    if request.method == "POST":
        # Accessing the data from request.POST
        doctor = Doctor.objects.create(
            first_name=request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            age=request.POST.get('age'),
            specialty = request.POST.get('specialty'),
            phone_number=request.POST.get('phone_number'),
            email = request.POST.get('email'),
            address = request.POST.get('address'),
            years_of_experience=request.POST.get('years_of_experience'),
        )
        # No need to call save() again since create() already saves the instance
        return redirect('doctor_list')  # Use the named URL pattern for the patient list

    return redirect('doctor_list')  # Fallback redirect for non-POST requests

# For Merge sort worker
# hospital_management/utils.py
def sorted_workers_list(request):
    # Retrieve all workers from the database
    workers = list(Worker.objects.all())
    
    # Sort workers by years of experience
    sorted_workers = merge_sort_workers(workers)
    
    # Pass sorted workers to the template
    return render(request, 'sorted_workers.html', {'workers': sorted_workers})

def delete_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    worker.delete()
    return redirect('worker_list')

def create_worker(request):
    if request.method == "GET":
        return render(request, 'createWorker.html')
    
    if request.method == "POST":
        # Accessing the data from request.POST
        worker = Worker.objects.create(
            first_name=request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            age=request.POST.get('age'),
            specialty = request.POST.get('specialty'),
            phone_number=request.POST.get('phone_number'),
            email = request.POST.get('email'),
            address = request.POST.get('address'),
            years_of_experience=request.POST.get('years_of_experience'),
        )
        # No need to call save() again since create() already saves the instance
        return redirect('worker_list')  # Use the named URL pattern for the patient list

    return redirect('worker_list')  # Fallback redirect for non-POST requests

#For shortest path algorithm 
def shortest_path_view(request):
    if request.method == "POST":
        form = ShortestPathForm(request.POST)
        if form.is_valid():
            start_location = form.cleaned_data['start']
            end_location = form.cleaned_data['end']
            path, total_distance = dijkstra_shortest_path(start_location.id, end_location.id)

            # Convert path IDs to location names
            location_names = [Location.objects.get(id=loc_id).name for loc_id in path]
            return render(request, 'shortest_path.html', {
                'form': form,
                'path': location_names,
                'total_distance': total_distance,
                'start_location': start_location,
                'end_location': end_location,
            })

    form = ShortestPathForm()
    return render(request, 'shortest_path.html', {'form': form})