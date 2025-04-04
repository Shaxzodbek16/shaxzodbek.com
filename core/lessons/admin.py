from django.contrib import admin

from lessons.models import Topic, StepsOfLesson, Lesson

admin.site.register(Lesson)
admin.site.register(Topic)
admin.site.register(StepsOfLesson)
