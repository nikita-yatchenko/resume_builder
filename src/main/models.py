from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ResumeData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    experience = models.TextField(blank=True)
    resume_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')

    def __str__(self):
        return self.user.username
