from django.db import models

# Create your models here.
from django.urls import reverse


class Register(models.Model):
    name = models.TextField(help_text="Name")
    usn = models.TextField(help_text="USN", primary_key=True)
    email = models.EmailField(help_text="Email (Use CMRIT Email)")
    score1 = models.TextField(help_text="Test 1 Score")
    score2 = models.TextField(help_text="Test 2 Score")
    score3 = models.TextField(help_text="Test 3 Score")
    score4 = models.TextField(help_text="Test 4 Score")

    def __str__(self):
        return self.usn

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])


class Meta:
    ordering = ['usn']




