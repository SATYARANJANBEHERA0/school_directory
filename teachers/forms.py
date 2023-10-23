from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'  # or specify the fields you want to include
class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()