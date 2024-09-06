from django import forms
from Maungawhau.models import CourseClass


class CreateForm(forms.ModelForm):
    class Meta:
        model = CourseClass
        fields = ('course', 'lecturers')
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),  # 'courses' -> 'course'
            'lecturers': forms.Select(attrs={'class': 'form-control'}),
        }
