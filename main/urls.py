from django.urls import path
from .views import AllLessonsAPIView, LessonsOfConcreteProductAPIView, ProductStatisticsAPIView

urlpatterns = [
    path('lessons/', AllLessonsAPIView.as_view(), name='all-lessons'),
    path('product_lessons/<int:id>', LessonsOfConcreteProductAPIView.as_view(), name='product-lessons'),
    path('products/statistics/', ProductStatisticsAPIView.as_view(), name='products-statistics')
]