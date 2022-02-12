from django.db import models
from django.conf import settings


class Laba8Result(models.Model):
    title = models.TextField()
    img_before = models.ImageField(upload_to='images/laba_8')
    img_after = models.ImageField(upload_to='images/laba_8')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return self.title