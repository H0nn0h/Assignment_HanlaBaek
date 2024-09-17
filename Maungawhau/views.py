from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from Maungawhau.models import CourseClass, Semester, Course, Lecturer, Profile, Student, CollegeDay
from Maungawhau.forms import createCourseClassForm, createLecturerForm, createCoursesForm, createSemestersForm, \
    createStudentsForm, createCollegeDaysForm
from django.contrib.auth.models import User

from django.db.models import Q
from django.views.generic import ListView
import pandas as pd


# Create your views here.

class HomeView(ListView):
    model = CourseClass
    template_name = 'home.html'
    ordering = ['-created_at']


class ClassDetailView(DetailView):
    model = CourseClass
    template_name = 'class_detail.html'
    context_object_name = 'courseClass'


class LecturerDetailView(DetailView):
    model = Lecturer
    template_name = 'lecturer_detail.html'


class StudentDetailView(DetailView):
    model = Student
    template_name = 'student_detail.html'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'


class SemesterDetailView(DetailView):
    model = Semester
    template_name = 'semester_detail.html'


class CollegeDayDetailView(DetailView):
    model = CollegeDay
    template_name = 'collegeday_detail.html'


class ClassCreateView(CreateView):
    model = CourseClass
    form_class = createCourseClassForm
    template_name = 'class_create.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('class_list')


class CourseCreateView(CreateView):
    model = Course
    form_class = createCoursesForm
    template_name = 'course_create.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('course_list')


class SemesterCreateView(CreateView):
    model = Semester
    form_class = createSemestersForm
    template_name = 'semester_create.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('semester_list')


class CollegeDayCreateView(CreateView):
    model = CollegeDay
    form_class = createCollegeDaysForm
    template_name = 'collegeday_create.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('collegeday_list')


# generate unique username
def gen_unique_username(first_name, last_name, dob):
    base_username = f"{first_name[0].lower()}{last_name.lower()}{dob.year}"
    username = base_username
    counter = 1

    while User.objects.filter(username=username).exists():
        username = f'{base_username}{counter}'
        counter += 1

    return username


class LecturerCreateView(CreateView):
    model = Lecturer
    form_class = createLecturerForm
    template_name = 'lecturer_create.html'
    success_url = reverse_lazy('lecturer_list')

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        dob = form.cleaned_data['DOB']

        username = gen_unique_username(first_name, last_name, dob)

        default_password = dob.strftime('%d%m%Y')  # ddmmyyyy 형식으로 변환

        # User 객체 생성
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=default_password  # 비밀번호 설정
        )

        # Lecturer와 User를 연결
        lecturer = form.save(commit=False)  # Lecturer 객체를 생성하되, 아직 DB에 저장하지 않음
        lecturer.user = user  # User와 연결
        lecturer.save()  # Lecturer 객체 저장

        return super().form_valid(form)


class StudentCreateView(CreateView):
    model = Student
    form_class = createStudentsForm
    template_name = 'student_create.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        # 유저 먼저 생성
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        dob = form.cleaned_data['DOB']

        username = gen_unique_username(first_name, last_name, dob)

        default_password = dob.strftime('%d%m%Y')
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(default_password)
        user.save()

        # Student와 User를 연결
        student = form.save(commit=False)
        student.user = user  # User와 연결
        student.save()

        return super().form_valid(form)


class ClassUpdateView(UpdateView):
    model = CourseClass
    fields = ['number', 'course', 'semester', 'lecturers']
    template_name = 'class_update.html'
    context_object_name = 'courseClass'
    success_url = '/class_list/'


class SemesterUpdateView(UpdateView):
    model = Semester
    form_class = createSemestersForm
    template_name = 'semester_update.html'
    context_object_name = 'semester'
    success_url = reverse_lazy('semester_list')


class CollegedayUpdateView(UpdateView):
    model = CollegeDay
    form_class = createCollegeDaysForm
    template_name = 'collegeday_update.html'
    context_object_name = 'collegeday'
    success_url = reverse_lazy('collegeday_list')


class LecturerUpdateView(UpdateView):
    model = Lecturer
    form_class = createLecturerForm
    template_name = 'lecturer_update.html'
    context_object_name = 'lecturer'
    success_url = reverse_lazy('lecturer_list')

    def get_success_url(self):
        return f'/lecturer_detail/{self.object.id}/'


class StudentUpdateView(UpdateView):
    model = Student
    form_class = createStudentsForm
    template_name = 'student_update.html'
    context_object_name = 'student'
    success_url = reverse_lazy('student_list')

    def get_success_url(self):
        return f'/student_detail/{self.object.id}/'


class CourseUpdateView(UpdateView):
    model = Course
    form_class = createCoursesForm
    template_name = 'course_update.html'
    context_object_name = 'course'
    success_url = reverse_lazy('course_list')

    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'pk': self.object.pk})


class ClassListView(ListView):
    model = CourseClass
    template_name = 'class_list.html'
    context_object_name = 'courseClasses'


class SemesterListView(ListView):
    model = Semester
    template_name = 'semester_list.html'
    context_object_name = 'semesters'


class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'

class CollegedayListView(ListView):
    model = CollegeDay
    template_name = 'collegeday_list.html'
    context_object_name = 'collegedays'

class LecturerListView(ListView):
    model = Lecturer
    template_name = 'lecturer_list.html'
    context_object_name = 'lecturers'


def lecturer_list(request):
    lecturers = Lecturer.objects.all()
    return render(request, 'lecturer_list.html', {'lecturers': lecturers})


class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'


def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})


class ClassDeleteView(DeleteView):
    model = CourseClass
    template_name = 'class_delete.html'

    def get_success_url(self):
        return reverse_lazy('class_list')


class SemesterDeleteView(DeleteView):
    model = Semester
    template_name = 'semester_delete.html'

    def get_success_url(self):
        return reverse_lazy('semester_list')


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'course_delete.html'

    def get_success_url(self):
        return reverse_lazy('course_list')


class LecturerDeleteView(DeleteView):
    model = Lecturer
    template_name = 'lecturer_delete.html'

    def get_success_url(self):
        return reverse_lazy('lecturer_list')


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_delete.html'

    def get_success_url(self):
        return reverse_lazy('students_list')


def create_class(request):
    if request.method == 'GET':
        semesters = Semester.objects.all()
        courses = Course.objects.all()
        lecturers = Lecturer.objects.all()
        return render(request, 'class_create.html',
                      {'semesters': semesters,
                       'courses': courses,
                       'lecturers': lecturers, })

    class_number = request.POST.GET('class_number')
    semester_id = request.POST.get('semester_id')
    semester = Semester.objects.get(id=semester_id)
    course_id = request.POST.get('course_id')
    course = Course.objects.get(id=course_id)
    lecturer_id = request.POST.get('lecturer_id')
    lecturer = Lecturer.objects.get(id=lecturer_id)

    course = Course.objects.get(id=course_id)
    semester = Semester.objects.get(id=semester_id)
    lecturer = Lecturer.objects.get(id=lecturer_id)

    new_class = CourseClass.objects.create(
        number=class_number,
        semester=semester,
        course=course,
        lecturers=lecturer
    )

    return render(request, 'class_create.html')


def create_lecturer(request):
    if request.method == 'POST':
        form = createLecturerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lecturer_list')
    else:
        form = createLecturerForm()
    return render(request, 'lecturer_create.html')


def create_student(request):
    if request.method == 'POST':
        form = createStudentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = createStudentsForm()
    return render(request, 'student_create.html')


def create_courses(request):
    if request.method == 'POST':
        form = createCoursesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = createCoursesForm()
    return render(request, 'course_create.html')


def create_semester(request):
    if request.method == 'POST':
        form = createSemestersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('semester_list')
    else:
        form = createSemestersForm()
    return render(request, 'semester_create.html')


# need to make connection with student
def attend_or_not(request):
    if request.method == 'POST':
        courseClass_id = request.POST.get('course_id')
        courseClass = CourseClass.objects.get(id=courseClass_id)
        # 참석 추가/제거 처리
        if request.user in courseClass.attendances.all():
            courseClass.attendances.remove(request.user)
        else:
            courseClass.attendances.add(request.user)

        return render(request, 'class_detail.html', {'object': courseClass})


class ProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user_profile'


def create_profile(request):
    if request.method == 'GET':
        return render(request, 'create_profile.html')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    user = User.objects.get(id=request.user.id)
    Profile.objects.create(user=user, phone=phone, address=address)
    return render(request, 'profile.html',
                  {'object': user})


def register_user(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    username = request.POST.get('username')
    if username in User.objects.values_list('username', flat=True):
        return render(request, 'register.html',
                      {'error': 'Username already exist'})
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    if password1 != password2:
        return render(request, 'register.html',
                      {'error': 'Passwords do not match'})
    if User.objects.create_user(username=username, email=email,
                                first_name=first_name, last_name=last_name):
        user = User.objects.get(username=username)
        user.set_password(password1)
        user.save()
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        Profile.objects.create(user=user, phone=phone, address=address)
        return render(request, 'registration/login.html')
    else:
        return render(request, 'register.html',
                      {'error': 'Something went wrong'})


def load_user_from_file(request):
    if request.method == 'GET':
        return render(request, 'load_user_from_file.html')
    file = request.FILES.get('file')
    if not file:
        return HttpResponse("No file uploaded", status=400)

    try:
        # 엑셀 파일 읽기
        excel_file = pd.read_excel(file, sheet_name=None)
        student_data = pd.DataFrame(excel_file['Student'])
        course_class_data = pd.DataFrame(excel_file['CourseClass'])

        # 학생 정보 처리
        student_first_names = student_data['first_name'].values.tolist()
        student_last_names = student_data['last_name'].values.tolist()
        student_emails = student_data['email'].values.tolist()
        student_dobs = student_data['DOB'].values.tolist()
        for i in range(len(student_first_names)):
            first_name = student_first_names[i]
            last_name = student_last_names[i]
            email = student_emails[i]
            dob = student_dobs[i]
            print(f"Student: {first_name} {last_name}, Email: {email}, DOB: {dob}")

        # CourseClass 정보 처리
        course_class_numbers = course_class_data['number'].values.tolist()
        course_class_courses = course_class_data['course'].values.tolist()
        for i in range(len(course_class_numbers)):
            number = course_class_numbers[i]
            course = course_class_courses[i]
            print(f"Course Class Number: {number}, Course: {course}")

        # 처리 완료 후 성공 메시지 반환
        return HttpResponse("File processed successfully")

    except Exception as e:
        # 예외 처리 및 에러 응답 반환
        print(f"Error processing file: {str(e)}")
        return HttpResponse(f"Error processing file: {str(e)}", status=500)
