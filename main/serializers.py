from rest_framework import serializers
from .models import LessonViewing, Lesson


    

class LessonViewingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonViewing
        fields = ['duration', 'status']


class LessonSerializer(serializers.ModelSerializer):
    viewing = serializers.IntegerField()
    status = serializers.CharField()

    class Meta:
        model = Lesson
        fields = ['name', 'url', 'duration', 'viewing', 'status']


class ProductLessonSerializer(LessonSerializer):
    date = serializers.DateField()

    class Meta:
        model = Lesson
        fields = ['name', 'url', 'duration', 'viewing', 'status', 'date']
