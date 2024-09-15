from profile import Profile

from django.contrib.auth.models import User
from django.db import models


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


class CourseClass(models.Model):
    number = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturers = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendances = models.ManyToManyField(User, related_name='course_class_attendances', blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f's{self.number} -{self.course.name}'

    def get_absolute_url(self):
        return f'/class_detail/{self.id}/'


class CollegeDay(models.Model):
    date = models.DateField()
    courseClass = models.ForeignKey(CourseClass, on_delete=models.CASCADE)

    def __str__(self):
        return f'college Day on {self.date} for {self.courseClass}'


class Student(models.Model):
    student_id = models.IntegerField(unique=True, blank=True, null=True)  # 6자리 숫자
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DOB = models.DateField()
    phone = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=255, default='')


    #email generate
    def save(self,*args, **kwargs):
        if not self.user.email:
            last_name =self.user.last_name.lower()
            first_name= self.user.first_name[0].lower()
            birth_day = str(self.DOB.day)
            email = f'{last_name}{first_name}{birth_day}@mymaungawhau.ac.nz'
            self.user.email = email
            self.user.save()

        super().save(*args, **kwargs)
    def __str__(self):
        return f'Student {self.user.first_name} {self.user.last_name}'


class Lecturer(models.Model):
    staff_id = models.IntegerField(unique=True, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DOB = models.DateField()
    phone = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=255, default='')

    def save(self, *args, **kwargs):
        # staff_id 자동 생성 로직
        if not self.staff_id:
            last_lecturer = Lecturer.objects.order_by('staff_id').last()  # 가장 최근에 생성된 Lecturer의 staff_id를 가져옴
            if last_lecturer and last_lecturer.staff_id:
                self.staff_id = last_lecturer.staff_id + 1  # staff_id를 이전 staff_id에 1을 더해 설정
            else:
                self.staff_id = 1000  # 첫 번째 Lecturer의 staff_id는 1000부터 시작

    #email generate
        if not self.user.email:
            last_name = self.user.last_name.lower()
            first_name = self.user.first_name[0].lower()
            birth_day =str(self.DOB.day)
            email = f'{last_name}{first_name}{birth_day}@staffmaungawhau.ac.nz'
            self.user.email = email
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Lecturer {self.user.first_name} {self.user.last_name}'

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_class = models.ForeignKey(CourseClass, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)