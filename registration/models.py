from django.db import models

# Create your models here.
from django.urls import reverse


class Instructions(models.Model):
    test_time = models.CharField(max_length=5, help_text="Enter the duration of the test")
    num_questions = models.CharField(max_length=5, help_text="Number of questions in the test")
    test_number = models.CharField(max_length=5, help_text="Test Number")
    test_name = models.CharField(max_length=25, help_text="Test Name")

    def __str__(self):
        return self.test_number

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.test_number)])


class Register(models.Model):
    name = models.CharField(help_text="Name", max_length=25)
    usn = models.CharField(help_text="USN", max_length=10)
    email = models.EmailField(help_text="Email (Use CMRIT Email)", max_length=25, primary_key=True,)
    score1 = models.CharField(help_text="Test 1 Score", max_length=5)
    score2 = models.CharField(help_text="Test 2 Score", max_length=5)
    score3 = models.CharField(help_text="Test 3 Score", max_length=5)
    score4 = models.CharField(help_text="Test 4 Score", max_length=5)
    score5 = models.CharField(help_text="Test 5 Score", max_length=5)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.usn)])


class Meta:
    ordering = ['email']





