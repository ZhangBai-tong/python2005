from django.urls import path, re_path
from course import views

urlpatterns = [
    path("category/", views.CourseCategoryAPIView.as_view()),
    path("courses/", views.CourseAPIView.as_view()),
    path("detail/<str:pk>/", views.CourseDetailAPIView.as_view()),
    path("chapters/", views.CourseChapterAPIView.as_view()),
]
