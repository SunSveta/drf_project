from django.contrib import admin

from newpro.models import Course, Lesson
from user.models import User

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(User)
