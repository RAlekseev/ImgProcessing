from django.db import models
from django.conf import settings
from jsonfield import JSONField


class Laba6Result(models.Model):
    title = models.TextField()
    text = models.TextField()
    font = models.TextField()
    img_before = models.ImageField(upload_to='images/laba_5')
    letters = JSONField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    i = 0

    def __str__(self):
        return self.title

    def order_letter(self):
        self.i += 1
        return self.text.replace(' ', '')[self.i-1]

    def hypo_letter(self):

        hypothesis = self.letters[self.i - 1]
        max_val = max(hypothesis.values())
        for key, value in hypothesis.items():
            if value == max_val:
                return key + ": (" + str(value) + ")"


    def final_text(self):
        final_text = ""
        for hypothesis in self.letters:
            final_text += max(hypothesis, key=hypothesis.get)

        return final_text
