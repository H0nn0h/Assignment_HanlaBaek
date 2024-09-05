from django import forms
from Maungawhau.models import CourseClass

class CreateForm(forms.ModelForm):
    class Meta:
        model = CourseClass
        fields = ( 'course','semester','lecturer')
        widgets={
              'course': forms.Select(attrs={'class':'form-control'}),
            'semester': forms.Select(attrs={'class':'form-control'}),
            'lecturer': forms.Select(attrs={'class':'form-control'}),
        }