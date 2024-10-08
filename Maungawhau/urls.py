from django import views
from django.urls import path

from Maungawhau.models import lecturer_attendance
from Maungawhau.views import HomeView, ClassDetailView, ClassUpdateView, ClassDeleteView, create_class, \
    attend_or_not, create_profile, register_user, load_user_from_file, ClassListView, SemesterDeleteView, \
    SemesterListView, CourseDeleteView, CourseListView, LecturerDeleteView, LecturerListView, StudentDeleteView, \
    StudentListView, SemesterCreateView, CourseCreateView, LecturerCreateView, StudentCreateView, LecturerUpdateView, \
    LecturerDetailView, CourseDetailView, CourseUpdateView, SemesterUpdateView, SemesterDetailView, StudentUpdateView, \
    StudentDetailView, ClassCreateView, college_day_create, college_day_create, CollegeDayListView, \
    student_attend_detail, lecturer_attend_detail

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('courseClass_create/', ClassCreateView.as_view(), name='class_create'),
    path('courseClass/<int:pk>/delete/', ClassDeleteView.as_view(), name='class_delete'),
    path('class_list/', ClassListView.as_view(), name='class_list'),
    path('courseClass/<int:pk>/update/', ClassUpdateView.as_view(), name='class_update'),
    path('courseClass_detail/<int:pk>/', ClassDetailView.as_view(), name='class_detail'),
    path('attend_or_not', attend_or_not, name='attend_or_not'),
    path('user_profile', create_profile, name='create_profile'),
    path('register/', register_user, name='register'),
    path('load_user_from_file/', load_user_from_file, name='load_user_from_file'),

    # Semester URLs
    path('semester_create/', SemesterCreateView.as_view(), name='semester_create'),
    path('semesters/<int:pk>/delete/', SemesterDeleteView.as_view(), name='semester_delete'),
    path('semesters/', SemesterListView.as_view(), name='semester_list'),
    path('semester/<int:pk>/update/', SemesterUpdateView.as_view(), name='semester_update'),
    path('semester_detail/<int:pk>/', SemesterDetailView.as_view(), name='semester_detail'),

    # Course URLs
    path('course_create/', CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('course_detail/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),

    # Lecturer URLs

    path('lecturer_create/', LecturerCreateView.as_view(), name='lecturer_create'),
    path('lecturers/<int:pk>/delete/', LecturerDeleteView.as_view(), name='lecturer_delete'),
    path('lecturers/', LecturerListView.as_view(), name='lecturer_list'),
    path('lecturer/<int:pk>/update/', LecturerUpdateView.as_view(), name='lecturer_update'),
    path('lecturer_detail/<int:pk>/', LecturerDetailView.as_view(), name='lecturer_detail'),

    # Student URLs

    path('student_create/', StudentCreateView.as_view(), name='student_create'),
    path('students/<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('student/<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
    path('student_detail/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),

    # CollegeDay URLs

    path('college_day_create/', college_day_create, name='college_day_create'),
    path('collegedays/', CollegeDayListView.as_view(), name='collegeDay_list'),
    path('college_day/<int:pk>/<int:student_id>/attendance/', attend_or_not, name='attend_or_not'),
    # attendances
    path('lecturer/attendance/', lecturer_attendance, name='lecturer_attendance'),
    path('student/<int:student_id>', student_attend_detail, name='student_attend_detail'),
    path('lecturer/<int:staff_id>/attendance', lecturer_attend_detail, name='lecturer_attend_detail')
]
