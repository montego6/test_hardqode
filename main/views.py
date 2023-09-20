from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LessonViewingSerializer, LessonSerializer
from .models import ProductAccess, LessonViewing, Lesson


class AllLessonsAPIView(APIView):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'not authenticated'})
        all_lessons = Lesson.objects.filter(products__accesses__user=user)
        print(all_lessons.query)
        serializer = LessonSerializer(all_lessons, many=True, context={'user': request.user})
        return Response(serializer.data)
# Create your views here.
