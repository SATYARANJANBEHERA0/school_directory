from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Teacher
from .serializers import TeacherSerializer
import csv

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher
from .forms import TeacherForm, CSVUploadForm
from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teachers_list.html', {'teachers': teachers})

def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})

def teacher_form(request, teacher_id=None):
    if teacher_id is not None:
        teacher = get_object_or_404(Teacher, pk=teacher_id)
    else:
        teacher = None

    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)

    return render(request, 'teachers/teacher_form.html', {'form': form})


#  bulk file upload

import csv
from django.db.utils import IntegrityError  # Import IntegrityError
from django.shortcuts import render, redirect
from .models import Teacher,Subject
from .forms import CSVUploadForm
from django.db.models import Q
from .models import Teacher, Subject

def bulk_upload(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

            next(csv_data, None)  # Skip the header row if present in the CSV

            for row in csv_data:
                first_name, last_name, profile_picture, email, phone_number, room_number, subjects_taught = row

                # Split the subjects_taught into a list
                subjects_list = [subject.strip() for subject in subjects_taught.split(',')]

                # Create or get the Teacher object
                teacher, created = Teacher.objects.get_or_create(
                    email=email,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'profile_picture': profile_picture,
                        'phone_number': phone_number,
                        'room_number': room_number,
                    }
                )

                # Process and create Subject objects and assign them to the teacher
                for subject_name in subjects_list:
                    subject, created = Subject.objects.get_or_create(name=subject_name)
                    teacher.subjects_taught.add(subject)

            return redirect('teacher_list')
    else:
        form = CSVUploadForm()

    return render(request, 'teachers/bulk_upload.html', {'form': form})
