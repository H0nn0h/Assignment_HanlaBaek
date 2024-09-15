from django import views
from django.urls import path
from Maungawhau.views import HomeView, ClassDetailView, ClassCreateView, ClassUpdateView, ClassDeleteView, create_class, \
    attend_or_not, create_profile, register_user, load_user_from_file, ClassListView, SemesterDeleteView, \
    SemesterListView, CourseDeleteView, CourseListView, LecturerDeleteView, LecturerListView, StudentDeleteView, \
    StudentListView, SemesterCreateView, CourseCreateView, LecturerCreateView, StudentCreateView, LecturerUpdateView, \
    LecturerDetailView, CourseDetailView, CourseUpdateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('class_detail/<int:pk>/', ClassDetailView.as_view(), name='class_detail'),
    path('class_create/', ClassCreateView.as_view(), name='class_create'),
    path('class_update/<int:pk>/', ClassUpdateView.as_view(), name='class_update'),
    path('class_delete/<int:pk>/', ClassDeleteView.as_view(), name='class_delete'),
    path('classes/', ClassListView.as_view(), name='class_list'),
    path('attend_or_not', attend_or_not, name='attend_or_not'),
    path('user_profile', create_profile, name='create_profile'),
    path('register/', register_user, name='register'),
    path('load_user_from_file/', load_user_from_file, name='load_user_from_file'),

    # Semester URLs
    path('semester_create/', SemesterCreateView.as_view(), name='semester_create'),
    path('semesters/<int:pk>/delete/', SemesterDeleteView.as_view(), name='semester_delete'),
    path('semesters/', SemesterListView.as_view(), name='semester_list'),

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

]
