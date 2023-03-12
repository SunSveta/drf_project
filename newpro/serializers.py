from rest_framework import serializers

from newpro.models import Course, Lesson, Subscription


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if 'youtube.com' not in value.get('video_link'):
            raise serializers.ValidationError('Левая ссылка')



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id','title', 'description', 'video_link',)
        validators = [LinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    #lesson_count = serializers.SerializerMethodField()
    #lessons = LessonSerializer(source='lesson_set', many=True)
    #subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'preview',
            'description',
            'price'
            #'lesson_count',
            #'lessons'
        )



    # def get_subscription(self, course):
    #     user = self.context['request'].user.id
    #
    #     subs = Subscription.objects.filter(course_id=course.id).filter(user_id=user)
    #     if subs:
    #         return 'active'
    #     return 'inactive'

    # def get_lesson_count(self, instance):
    #     #return Lesson.get_lesson_count(instance)
    #     return instance.lesson_get.count()  #из решения домашки от Олега  SET??

    # another version
    # def get_lesson_count(self, instance):
    #     lesson_object = Lesson.objects.filter(course_title=instance)
    #     if lesson_object:
    #         return lesson_object.count()
    #     return 0


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'course_id', 'status')

    def create(self, validated_data):
        new_subscription = Subscription.objects.create(**validated_data)
        return new_subscription




