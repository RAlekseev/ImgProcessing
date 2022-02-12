from django.db import models
from django.conf import settings
from jsonfield import JSONField


class Laba9Result(models.Model):
    title = models.TextField()
    voice = models.FileField(upload_to='images/laba_9')
    freq_min = models.FloatField()
    freq_max = models.FloatField()
    pow_timbre = models.FloatField()
    formants = JSONField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return self.title