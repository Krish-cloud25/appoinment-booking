# CI/CD test deployment run ✅
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile, Appointment, TriageForm, Doctor
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'appointments/home.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, role=role)
        return redirect('login')
    return render(request, 'appointments/signup.html')


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            role = user.profile.role
            if role == 'patient':
                return redirect('book')
            elif role == 'doctor':
                return render(request, 'appointments/doctor_dashboard.html')
            elif role == 'admin':
                return redirect('dashboard')
        else:
            return render(request, 'appointments/login.html', {'error': 'Invalid credentials'})
    return render(request, 'appointments/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def book_appointment(request):
    if request.method == 'POST':
        name = request.user.username  # 🛠 patient name from logged-in user
        age = int(request.POST['age'])
        symptoms = request.POST['symptoms']
        symptom1 = 'symptom1' in request.POST
        symptom2 = 'symptom2' in request.POST
        symptom3 = 'symptom3' in request.POST

        # Calculate urgency score
        score = sum([symptom1, symptom2, symptom3]) * 10

        # Only use available doctors
        doctor = Doctor.objects.filter(available=True).first()

        Appointment.objects.create(
            patient_name=name,
            age=age,
            symptoms=symptoms,
            urgency_score=score,
            doctor=doctor
        )

        return render(request, 'appointments/confirmation.html', {
            'name': name,
            'score': score
        })

    return render(request, 'appointments/book.html')


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient_name=request.user.username)
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})


@login_required
def edit_my_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient_name=request.user.username)
    if request.method == 'POST':
        appointment.age = int(request.POST['age'])
        appointment.symptoms = request.POST['symptoms']
        appointment.save()
        return redirect('my_appointments')
    return render(request, 'appointments/edit_my_appointment.html', {'appointment': appointment})


@login_required
def delete_my_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient_name=request.user.username)
    appointment.delete()
    return redirect('my_appointments')


@login_required
def dashboard(request):
    if request.user.profile.role != 'admin':
        return redirect('home')

    appointments = Appointment.objects.all().order_by('-urgency_score')
    return render(request, 'appointments/dashboard.html', {'appointments': appointments})


@login_required
def edit_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.patient_name = request.POST['name']
        appointment.age = int(request.POST['age'])
        appointment.symptoms = request.POST['symptoms']
        appointment.save()
        return redirect('dashboard')
    return render(request, 'appointments/edit.html', {'appointment': appointment})


@login_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    return redirect('dashboard')
