from django.db import models

# Create your models here.
from django.urls import reverse


class Quiz(models.Model):
    img = models.ImageField(primary_key=True)
    ans = models.TextField(help_text="Answer")
    exp = models.TextField(help_text="Explanation")
    cat = models.TextField(help_text="Category")

    def __str__(self):
        return self.img

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])


class Meta:
    ordering = ['cat']




