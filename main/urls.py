from django.urls import path
from .views import AllLessonsAPIView

urlpatterns = [
    path('lessons/', AllLessonsAPIView.as_view(), name='all-lessons')
]