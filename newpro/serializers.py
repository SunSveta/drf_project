from rest_framework import serializers

from newpro.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True)

    class Meta:
        model = Course
        fields = (
            'title',
            'preview',
            'description',
            'lesson_count',
            'lessons'
        )

    def get_lesson_count(self, instance):
        return Lesson.get_lesson_count(instance)


