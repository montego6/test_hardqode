from rest_framework import serializers
from .models import LessonViewing, Lesson, Product


    

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

class ProductStatisticsSerializer(serializers.ModelSerializer):
    lesson_views = serializers.IntegerField()
    total_duration = serializers.IntegerField()
    students_studying = serializers.IntegerField()
    selling_percentage = serializers.DecimalField(max_digits=4, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Product
        fields = ['id', 'lesson_views', 'total_duration', 'students_studying', 'selling_percentage']

