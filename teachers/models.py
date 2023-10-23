from django.db import models

# Create your models here.
 

class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    room_number = models.CharField(max_length=10)
    subjects_taught = models.ManyToManyField('Subject', related_name='teachers', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
