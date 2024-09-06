from django.urls import path
from Maungawhau.views import HomeView, ClassDetailView, ClassCreateView, ClassUpdateView, ClassDeleteView, create_class

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('class_detail/<int:pk>/', ClassDetailView.as_view(), name='class_detail'),
    path('class_create', ClassCreateView.as_view(), name='class_create'),
    path('class_update/<int:pk>/', ClassUpdateView.as_view(), name='class_update'),
    path('class_delete/<int:pk>/', ClassDeleteView.as_view(), name='class_delete'),
    path('class_create', create_class, name='class_create_function'),

]