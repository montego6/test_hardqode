from django.shortcuts import render
from django.db.models import OuterRef, Subquery
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LessonSerializer, ProductLessonSerializer
from .models import LessonViewing, Lesson, ProductAccess


class AllLessonsAPIView(APIView):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'not authenticated'})
        viewing = LessonViewing.objects.filter(lesson=OuterRef('pk'), user=user).order_by('-date')
        all_lessons = Lesson.objects.filter(products__accesses__user=user).annotate(viewing=Subquery(viewing.values('duration')[:1]), status=Subquery(viewing.values('status')[:1]))
        serializer = LessonSerializer(all_lessons, many=True)
        return Response(serializer.data)
    

class LessonsOfConcreteProductAPIView(APIView):
    def get(self, request, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'not authenticated'})
        id = kwargs.get('id')
        if not ProductAccess.objects.filter(product_id=id, user=user).exists():
            return Response({'detail': 'no access'})
        viewing = LessonViewing.objects.filter(lesson=OuterRef('pk'), user=user)
        lessons = Lesson.objects.filter(products__id=id).annotate(viewing=Subquery(viewing.values('duration')[:1]), status=Subquery(viewing.values('status')[:1]), date=Subquery(viewing.values('date')[:1]))
        serializer = ProductLessonSerializer(lessons, many=True)
        return Response(serializer.data)