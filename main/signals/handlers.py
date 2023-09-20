from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models import LessonViewing, Lesson

@receiver(pre_save, sender=LessonViewing)
def set_viewing_status(sender, instance, **kwargs):
    if instance.duration >= 0.8 * instance.lesson.duration:
        instance.status = LessonViewing.ViewingStatus.VIEWED