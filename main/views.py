from django.shortcuts import render
from django.db import models
from django.db.models import OuterRef, Subquery, Count, Q, Sum
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LessonSerializer, ProductLessonSerializer, ProductStatisticsSerializer
from .models import LessonViewing, Lesson, ProductAccess, Product

User = get_user_model()

class SubqueryCount(Subquery):
    template = f"(SELECT count(*) FROM (%(subquery)s)) * 1.0 / {User.objects.filter(is_staff=False).count()} * 100"
    output_field = models.DecimalField(max_digits=4, decimal_places=2)


class AllLessonsAPIView(APIView):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'not authenticated'})
        viewing = LessonViewing.objects.filter(lesson=OuterRef('pk'), user=user).order_by('-date')
        lessons = Lesson.objects.filter(products__accesses__user=user).annotate(viewing=Subquery(viewing.values('duration')[:1]), status=Subquery(viewing.values('status')[:1]))
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
    

class LessonsOfConcreteProductAPIView(APIView):
    def get(self, request, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'not authenticated'})
        id = kwargs.get('id')
        if not ProductAccess.objects.filter(product_id=id, user=user).exists():
            return Response({'detail': 'no access'})
        viewing = LessonViewing.objects.filter(lesson=OuterRef('pk'), user=user).order_by('-date')
        lessons = Lesson.objects.filter(products__id=id).annotate(viewing=Subquery(viewing.values('duration')[:1]), status=Subquery(viewing.values('status')[:1]), date=Subquery(viewing.values('date')[:1]))
        serializer = ProductLessonSerializer(lessons, many=True)
        return Response(serializer.data)
    

class ProductStatisticsAPIView(APIView):
    def get(self, request):
        # lesson_views = LessonViewing.objects.filter(lesson__products__id=OuterRef('pk'), status=LessonViewing.ViewingStatus.VIEWED).aggregate(c=Count('id'))
        # products = Product.objects.all().annotate(lesson_views=Subquery(lesson_views.values('c'), output_field=models.IntegerField()))
        accesses = ProductAccess.objects.filter(product__id=OuterRef('pk'))
        products = Product.objects.all().annotate(
            lesson_views=Count('lessons__viewings', filter=Q(lessons__viewings__status=LessonViewing.ViewingStatus.VIEWED)),
            total_duration=Sum('lessons__viewings__duration'),
            students_studying=Count('lessons__viewings', filter=Q(lessons__viewings__status=LessonViewing.ViewingStatus.NOTVIEWED)),
            selling_percentage=SubqueryCount(accesses)
            )
        #  / User.objects.filter(is_staff=False).count()) * 100
        # filter=Q(lessons__viewings__status=LessonViewing.ViewingStatus.NOTVIEWED)
        # products = products.annotate(total_duration=Sum('lessons__viewings__duration')).annotate(students_studying=Count('accesses', filter=Q(lessons__viewings__status=LessonViewing.ViewingStatus.NOTVIEWED)))

        serializer = ProductStatisticsSerializer(products, many=True)
        #  | Q(accesses__id__isnull=False)
        return Response(serializer.data)