from rest_framework import serializers
from .models import LessonViewing, Lesson


    

class LessonViewingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonViewing
        fields = ['duration', 'status']


class LessonSerializer(serializers.ModelSerializer):
    viewing = serializers.SerializerMethodField()

    def get_viewing(self, obj):
        user = self.context.get('user')
        viewing = LessonViewing.objects.get(user=user, lesson=obj)
        return LessonViewingSerializer(viewing).data

    class Meta:
        model = Lesson
        fields = ['name', 'url', 'duration', 'viewing']