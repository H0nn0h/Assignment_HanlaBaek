from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Semester(models.Model):
    year = models.IntegerField()
    semester =models.CharField(max_length =10)
    courses = models.ManyToManyField(Course, related_name='semesters', blank=True)

    def __str__(self):
        return self.semester

class CourseClass(models.Model):
    number = models.IntegerField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    lecturers = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField(User, related_name='course_class_students',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendances = models.ManyToManyField(User, related_name='course_class_attendances',blank=True)

    def __str__(self):
        return f's{self.number} -{self.course.name}'

    def get_absolute_url(self):
        return f'/class_detail/{self.id}/'

class CollegeDay(models.Model):
    date = models.DateField()
    courseClass = models.ForeignKey(CourseClass,on_delete=models.CASCADE)
    students= models.ManyToManyField(User, related_name='college_day_students',blank=True)

    def __str__(self):
        return f'college Day on {self.date} for {self.courseClass}'

class Student(models.Model):
    student_id = models.IntegerField()
    DOB = models.DateField()
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'student by{self.student_id} '

class Lecturer(models.Model):
    staff_id = models.IntegerField()
    DOB = models.DateField()
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'lecture by{self.staff_id} '

