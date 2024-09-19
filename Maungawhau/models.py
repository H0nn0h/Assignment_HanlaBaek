from profile import Profile

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render
from django.views import View


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} Profile'


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Semester(models.Model):
    year = models.IntegerField()
    semester = models.CharField(max_length=10)
    courses = models.ManyToManyField(Course, related_name='semesters', blank=True)

    def __str__(self):
        return self.semester


def save_user_email(user, dob, email_domain):
    """User의 이메일을 생성 및 저장하는 함수"""
    if not user.email:
        last_name = user.last_name.lower()
        first_name = user.first_name[0].lower()
        birth_day = str(dob.day)
        email = f'{last_name}{first_name}{birth_day}@{email_domain}'
        user.email = email
        user.save()


class Student(models.Model):
    student_id = models.IntegerField(unique=True, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DOB = models.DateField()
    phone = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=255, default='')

    def __str__(self):
        # 유저의 이름과 성을 반환하도록 설정
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        # student_id 자동 생성 로직만 유지
        if not self.student_id:
            last_student = Student.objects.order_by('student_id').last()
            if last_student and last_student.student_id:
                self.student_id = last_student.student_id + 1
            else:
                self.student_id = 100000  # 첫 번째 student_id는 100000부터 시작

        save_user_email(self.user, self.DOB, 'mymaungawhau.ac.nz')

        super().save(*args, **kwargs)


class Lecturer(models.Model):
    staff_id = models.IntegerField(unique=True, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DOB = models.DateField()
    phone = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=255, default='')

    def __str__(self):
        # 유저의 이름과 성을 반환하도록 설정
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        # staff_id 자동 생성 로직만 유지
        if not self.staff_id:
            last_lecturer = Lecturer.objects.order_by('staff_id').last()
            if last_lecturer and last_lecturer.staff_id:
                self.staff_id = last_lecturer.staff_id + 1
            else:
                self.staff_id = 1000  # 첫 번째 staff_id는 1000부터 시작

        save_user_email(self.user, self.DOB, 'staffmaungawhau.ac.nz')

        super().save(*args, **kwargs)


class CourseClass(models.Model):
    number = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturers = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendances = models.ManyToManyField(User, related_name='course_class_attendances', blank=True)

    def __str__(self):
        return f'{self.semester.semester}_{self.number} - {self.course.name}'

    def get_absolute_url(self):
        return f'/class_detail/{self.id}/'


class CollegeDay(models.Model):
    student = models.ManyToManyField(Student, blank=True)
    courseClass = models.ForeignKey(CourseClass, on_delete=models.CASCADE)
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday')
        ],
        default='Monday'
    )

    def __str__(self):
        return f'{self.student} - {self.courseClass} ({self.day_of_week})'


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    college_day = models.ForeignKey(CollegeDay, on_delete=models.CASCADE)
    course_class = models.ForeignKey(CourseClass, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')

    def __str__(self):
        return f"{self.student.username} - {self.course_class.name} on {self.college_day.date}"

    class Meta:
        permissions = [
            ("can_view_lecturer_attendance", "Can view lecturer attendance"),
            ("can_enter_attendance", "Can enter attendance"),
        ]

def lecturer_attendance(request):
    # logic for the view
    return render(request, 'lecturer_attendance.html')

class LecturerAttendanceView(View):
    def get(self, request):
        # logic for GET requests
        return render(request, 'lecturer_attendance.html')