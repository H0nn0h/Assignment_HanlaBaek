from datetime import date

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from Maungawhau.models import Student, Course, Lecturer, CourseClass, CollegeDay, Semester

# Register your models here.
# admin.site.register(Student)
# admin.site.register(Course)
# admin.site.register(Lecturer)
# admin.site.register(CourseClass)
# admin.site.register(CollegeDay)

# admin.site.register(Semester)


def assign_to_group(modeladmin, request, queryset, group_name):
    group = Group.objects.get(name=group_name)
    for user in queryset:
        user.groups.add(group)
        modeladmin.message_user(request, f"Selected users have been added to {group_name}")

class GroupAdmin(BaseGroupAdmin):
    def get_users(self, obj):
        return ", ".join([user.username for user in obj.user_set.all()])

    get_users.short_description = "Users in this group"
    list_display = ('name','get_users')

def assign_to_admin_group(modeladmin, request, queryset):
    assign_to_group(modeladmin, request, queryset, 'Admin')


def assign_to_lecturer_group(modeladmin, request, queryset):
    group = Group.objects.get(name='Lecturer')
    for user in queryset:
        user.groups.add(group)


        if not Lecturer.objects.filter(user=user).exists():
            Lecturer.objects.create(user=user, DOB=date(1981, 10, 1))

        modeladmin.message_user(request, f"{user.username} has been added to Lecturer group and registered as Lecturer")


def assign_to_student_group(modeladmin, request, queryset):
    assign_to_group(modeladmin, request, queryset, 'Student')


assign_to_admin_group.short_description = "Add selected users to Admin group"
assign_to_student_group.short_description = "Add selected users to Student group"
assign_to_lecturer_group.short_description = "Add selected users to Lecturer group"

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'id', 'get_dob','is_staff')
    actions = [assign_to_admin_group, assign_to_lecturer_group, assign_to_student_group]

    def get_dob(self, obj):
        # Student 모델에 연결된 사용자에 대해서만 DOB를 표시
        if hasattr(obj, 'student'):
            return obj.student.DOB
        # Lecturer 모델에 연결된 사용자에 대해서만 DOB를 표시
        elif hasattr(obj, 'lecturer'):
            return obj.lecturer.DOB
        return None

    get_dob.short_description = 'Date of Birth'


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_id', 'DOB', 'phone', 'address')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'DOB', 'phone', 'address')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'semester')


@admin.register(CourseClass)
class CourseClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'lecturers', 'semester')

@admin.register(CollegeDay)
class CollegeDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_students', 'courseClass', 'day_of_week')

    def get_students(self, obj):
        return ", ".join([str(student) for student in obj.student.all()])
    get_students.short_description = 'Students'