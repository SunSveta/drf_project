from django.urls import path
from rest_framework.routers import DefaultRouter

from newpro.views import *

#from newpro.apps import NewproConfig
#app_name = NewproConfig.name

router = DefaultRouter()
router.register(r'newpro', CourseViewSet, basename='newpro')

urlpatterns = [
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/create', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/retrieve/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lesson/destroy/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson_destroy'),
              ] + router.urls