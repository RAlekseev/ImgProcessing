from django.db import models
from django.conf import settings
from jsonfield import JSONField


class Laba7Result(models.Model):
    title = models.TextField()
    img_before = models.ImageField(upload_to='images/laba_7')
    img_after = models.ImageField(upload_to='images/laba_7')
    evidence = JSONField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return self.title