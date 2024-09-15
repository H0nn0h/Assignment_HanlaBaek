from datetime import date

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User, Group
from Maungawhau.models import Student, Course, Lecturer, CourseClass, CollegeDay, Semester

# Register your models here.
admin.site.register(Student)
# admin.site.register(Course)
# admin.site.register(Lecturer)
admin.site.register(CourseClass)
admin.site.register(CollegeDay)
admin.site.register(Semester)


def assign_to_group(modeladmin, request, queryset, group_name):
    group = Group.objects.get(name=group_name)
    for user in queryset:
        user.groups.add(group)
        modeladmin.message_user(request, f"Selected users have been added to {group_name}")


def assign_to_admin_group(modeladmin, request, queryset):
    assign_to_group(modeladmin, request, queryset, 'Admin')


def assign_to_lecturer_group(modeladmin, request, queryset):
    group = Group.objects.get(name='Lecturer')
    for user in queryset:
        user.groups.add(group)

        # 동시에 Lecturer 모델에 등록
        if not Lecturer.objects.filter(user=user).exists():
            Lecturer.objects.create(user=user, DOB=date(1981,10,1))  # 필요시 DOB 등을 실제 데이터로 수정하세요

        modeladmin.message_user(request, f"{user.username} has been added to Lecturer group and registered as Lecturer")




def assign_to_student_group(modeladmin, request, queryset):
    assign_to_group(modeladmin, request, queryset, 'Student')


assign_to_admin_group.short_description = "Add selected users to Admin group"
assign_to_student_group.short_description = "Add selected users to Student group"
assign_to_lecturer_group.short_description = "Add selected users to Lecturer group and register as Lecturer"

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'id', 'get_dob')
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


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id','code','name')

