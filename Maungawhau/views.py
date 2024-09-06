from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from Maungawhau.models import CourseClass, Semester, Course, Lecturer
from Maungawhau.forms import CreateForm
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


class ClassCreateView(CreateView):
    model = CourseClass
    form_class = CreateForm
    template_name = 'class_create.html'


class ClassUpdateView(UpdateView):
    model = CourseClass
    form_class = CreateForm
    template_name = 'class_update.html'

    def get_success_url(self):
        return f'/class_detail/{self.object.id}/'


class ClassDeleteView(DeleteView):
    model = CourseClass
    template_name = 'class_delete.html'

    def get_success_url(self):
        return reverse_lazy('home')


def create_class(request):
    if request.method == 'GET':
        semesters = Semester.objects.all()
        return render(request, 'class_create.html', {'semesters': semesters})

    semester_id = request.POST.get('semester_id')
    semester = Semester.objects.get(id=semester_id)
    course_id = request.POST.get('course_id')
    course = Course.objects.get(id=course_id)
    student_id = request.POST.get('student_id')
    student = User.objects.get(id=student_id)
    lecturer_id = request.POST.get('lecturer_id')
    lecturer = Lecturer.objects.get(id=lecturer_id)

    new_class = CourseClass.objects.create(
        semester=semester,
        course=course,
        lecturers=lecturer
    )

    # 학생 추가
    new_class.students.add(student)

    return redirect(f'/class_detail/{new_class.id}/')


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
        courseClass = get_object_or_404(CourseClass, id=request.POST.get('course_id'))

        # 참석 추가/제거 처리
        if request.user in courseClass.attendances.all():
            courseClass.attendances.remove(request.user)
        else:
            courseClass.attendances.add(request.user)


        return HttpResponseRedirect(reverse('class_detail', args=[str(courseClass.id)]))
