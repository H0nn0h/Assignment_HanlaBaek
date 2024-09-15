from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from Maungawhau.models import CourseClass, Semester, Course, Lecturer, Profile, Student
from Maungawhau.forms import CreateForm, createLecturerForm, createCoursesForm
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


class LecturerDetailView(DetailView):
    model = Lecturer
    template_name = 'lecturer_detail.html'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'


class ClassCreateView(CreateView):
    model = CourseClass
    form_class = CreateForm
    template_name = 'class_create.html'


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
    form_class = CreateForm
    template_name = 'semester_create.html'


class LecturerCreateView(CreateView):
    model = Lecturer
    form_class = createLecturerForm
    template_name = 'lecturer_create.html'
    success_url = reverse_lazy('lecturer_list')

    def form_valid(self, form):
        lecturer = form.save(commit=False)
        user = lecturer.user
        dob = form.cleaned_data['DOB']
        default_password = dob.strftime('%d%m%Y')
        user.set_password(default_password)
        user.save()
        lecturer.save()
        return super().form_valid(form)


class StudentCreateView(CreateView):
    model = Student
    form_class = CreateForm
    template_name = 'student_create.html'


class ClassUpdateView(UpdateView):
    model = CourseClass
    form_class = CreateForm
    template_name = 'class_update.html'
    context_object_name = 'class'

    def get_success_url(self):
        return f'/class_detail/{self.object.id}/'


class LecturerUpdateView(UpdateView):
    model = Lecturer
    form_class = createLecturerForm
    template_name = 'lecturer_update.html'
    context_object_name = 'lecturer'
    success_url = reverse_lazy('lecturer_list')

    def get_success_url(self):
        return f'/lecturer_detail/{self.object.id}/'


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
    context_object_name = 'classes'


class SemesterListView(ListView):
    model = Semester
    template_name = 'semester_list.html'
    context_object_name = 'semesters'


class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'


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


def create_courses(request):
    if request.method == 'POST':
        form = createCoursesForm(request.Post)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = createCoursesForm()
    return render(request, 'course_create.html')


# search function
class SearchResultsView(ListView):
    model = CourseClass
    template_name = 'class_create.html'

    def get_queryset(self):
        query = self.request.GET.get('searched')
        return CourseClass.objects.filter(
            Q(number__icontains=query) |
            Q(course__name__icontains=query) |
            Q(semester__semester__icontains=query)
        )


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
