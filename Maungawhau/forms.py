from django import forms
from Maungawhau.models import CourseClass, Lecturer, Course, Semester, Student, CollegeDay


class createCourseClassForm(forms.ModelForm):
    class Meta:
        model = CourseClass
        fields = ('number', 'course', 'semester', 'lecturers')
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'})
        }
        course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Course')
        semester = forms.ModelChoiceField(queryset=Semester.objects.all(), label='Semester')

    lecturers = forms.ModelChoiceField(
        queryset=Lecturer.objects.all(),  # Lecturer로 필터링된 사용자만 표시
        label='Lecturer',
        required=False
    )


class createLecturerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Lecturer
        fields = ('first_name', 'last_name', 'DOB', 'phone', 'address')

        widgets = {
            'DOB': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(createLecturerForm, self).__init__(*args, **kwargs)
        if self.instance.pk:  # 이미 생성된 객체인 경우
            self.fields['staff_id'] = forms.CharField(
                initial=self.instance.staff_id, disabled=True, label="Staff ID", required=False)

    # User 모델의 first_name과 last_name을 처리
    def save(self, commit=True):
        lecturer = super().save(commit=False)
        if commit:
            lecturer.save()
        return lecturer


class createStudentsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'DOB', 'phone', 'address')

        widgets = {
            'student_id': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'DOB': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(createStudentsForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['student_id'] = forms.CharField(
                initial=self.instance.student_id, disabled=True, label="Student ID", required=False)

    # User 모델의 first_name과 last_name을 처리
    def save(self, commit=True):
        student = super().save(commit=False)
        if commit:
            student.save()
        return student


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
        if commit:
            course.save()
        return course


class createSemestersForm(forms.ModelForm):
    SEMESTER_CHOICES = [
        ('Semester 1', 'Semester 1'),
        ('Semester 2', 'Semester 2'),
    ]
    year = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    semester = forms.ChoiceField(choices=SEMESTER_CHOICES, required=True,
                                 widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Semester
        fields = ('year', 'semester')

        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        semester = super().save(commit=False)
        if commit:
            semester.save()
        return semester


class CollegeDayForm(forms.ModelForm):
    class Meta:
        model = CollegeDay
        fields = ['student', 'courseClass', 'day_of_week', 'attendance_status']

        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'attendance_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_day_of_week(self):
        day = self.cleaned_data['day_of_week']
        if day not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            raise forms.ValidationError("Please select a valid weekday.")
        return day