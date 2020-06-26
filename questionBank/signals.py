from django.contrib.auth.models import User
from django.db.models.signals import post_save
from . models import Student

def student_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(
            user = instance,
            name = instance.username,
            email = instance.email
        )


post_save.connect(student_profile, sender=User)
