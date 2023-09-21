from django.urls import path
from .views import UserLessonsAPIView, LessonsOfConcreteProductAPIView, ProductStatisticsAPIView

urlpatterns = [
    path('lessons/', UserLessonsAPIView.as_view(), name='all-lessons'),
    path('products/<int:id>/lessons/', LessonsOfConcreteProductAPIView.as_view(), name='product-lessons'),
    path('products/statistics/', ProductStatisticsAPIView.as_view(), name='products-statistics')
]