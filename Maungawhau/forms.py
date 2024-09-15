from django import forms
from Maungawhau.models import CourseClass, Lecturer, Course


class CreateForm(forms.ModelForm):
    class Meta:
        model = CourseClass
        fields = ('number', 'course', 'semester', 'lecturers')
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),  # 'courses' -> 'course'
            'semester': forms.Select(attrs={'semester': 'form-control'}),
            'lecturers': forms.Select(attrs={'class': 'form-control'}),

        }


class createLecturerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Username", max_length=30, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    class Meta:
        model = Lecturer
        fields = ('first_name', 'last_name', 'DOB', 'phone', 'address')

        widgets = {
            'staff_id': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'DOB': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(createLecturerForm, self).__init__(*args, **kwargs)
        if self.instance.pk:  # 이미 생성된 객체인 경우
            self.fields['staff_id'] = forms.CharField(
                initial=self.instance.staff_id, disabled=True, label="Staff ID", required=False)
            self.fields['username'].initial = self.instance.user.username  # user의 username 필드 추가

    # User 모델의 first_name과 last_name을 처리
    def save(self, commit=True):
        lecturer = super().save(commit=False)
        user = lecturer.user  # Lecturer와 연결된 User
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            lecturer.save()
        return lecturer


class createCoursesForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    code = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Course
        fields = ('code', 'name')

        widgets = {
            'name': forms.TextInput(attrs={'course': 'form-control'}),
            'code': forms.TextInput(attrs={'course': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(createCoursesForm, self).__init__(*args, **kwargs)
        if self.instance.pk:  # 이미 생성된 객체인 경우
            self.fields['code'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        course = super().save(commit=False)
        course.name = self.cleaned_data['name']
        course.code = self.cleaned_data['code']
        if commit:
            course.save()
        return course
