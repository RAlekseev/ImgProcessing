from django.db import models
from django.conf import settings


class Laba3Result(models.Model):
    title = models.TextField()
    img_before = models.ImageField(upload_to='images/laba_3')
    Gx = models.ImageField(upload_to='images/laba_3')
    Gy = models.ImageField(upload_to='images/laba_3')
    G = models.ImageField(upload_to='images/laba_3')
    img_after = models.ImageField(upload_to='images/laba_3')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return self.title