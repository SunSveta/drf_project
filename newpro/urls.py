from django.urls import path

from newpro.views import *
from newpro.apps import NewproConfig

app_name = NewproConfig.name


urlpatterns = [
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/create', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/retrieve/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lesson/destroy/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson_destroy'),
    path('list_course/',CourseListAPIView.as_view(),name='list_course'),
    path('create_course/',CourseCreateAPIView.as_view(),name='create_course'),
    path('update_course/<int:pk>/',CourseUpdateAPIView.as_view(),name='update_course'),
    path('destroy_course/<int:pk>/',CourseDestroyAPIView.as_view(),name='destroy_course'),
    path('retrieve_course/<int:pk>/',CourseRetrieveAPIView.as_view(),name='retrieve_course'),
              ]