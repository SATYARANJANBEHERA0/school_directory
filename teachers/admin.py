from django.contrib import admin
from .models import Teacher

# Define an Admin class for the Teacher model
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'room_number')
    list_filter = ('room_number', 'subjects_taught')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')

# Register the Teacher model with the admin site, using the custom TeacherAdmin class
admin.site.register(Teacher, TeacherAdmin)
