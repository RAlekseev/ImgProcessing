from django.db import models
from django.conf import settings
from jsonfield import JSONField
import os


class Laba5Result(models.Model):
    title = models.TextField()
    text = models.TextField()
    font = models.TextField()
    img_before = models.ImageField(upload_to='images/laba_5')
    prof_x = models.ImageField(upload_to='images/laba_5')
    prof_y = models.ImageField(upload_to='images/laba_5')
    prof_letters = JSONField()
    img_after = models.ImageField(upload_to='images/laba_5')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return self.title

    def profs(self):
        path = "/Users/jewelieee/Desktop/Bopai/media/images/laba_5/" + str(self.id) + "/char_profiles/original"
        img_list = os.listdir(path)
        return img_list