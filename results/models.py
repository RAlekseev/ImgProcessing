from django.db import models
from django.conf import settings


class Result(models.Model):
    title = models.TextField()
    img_before = models.ImageField(upload_to='images/')
    img_after = models.ImageField(upload_to='images/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return self.title