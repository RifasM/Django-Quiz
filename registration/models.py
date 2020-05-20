from django.db import models

# Create your models here.
from django.urls import reverse


class Instruction(models.Model):
    test_time = models.CharField(max_length=5, help_text="Enter the duration of the test")
    num_questions = models.CharField(max_length=5, help_text="Number of questions in the test")
    test_number = models.CharField(max_length=5, help_text="Test Number")
    test_name = models.CharField(max_length=25, help_text="Test Name")

    def __str__(self):
        return self.test_number


class Register(models.Model):
    name = models.CharField(help_text="Name", max_length=25)
    usn = models.CharField(help_text="USN", max_length=10)
    email = models.EmailField(help_text="Email", max_length=25, primary_key=True)
    group = models.CharField(help_text="Enter group", max_length=25)
    score = models.CharField(help_text="Test Score", max_length=5, blank=True)

    def __str__(self):
        return self.email

    """def get_absolute_url(self):
        # Returns the url to access a particular instance of the model.
        return reverse('model-detail-view', args=[str(self.usn)])
    """
    class Meta:
        ordering = ['email']


class Test(models.Model):
    test_num = models.AutoField(help_text="Test Number", primary_key=True)
    test_name = models.CharField(help_text="Enter Test Name", max_length=25)
    test_duration = models.CharField(help_text="Enter Test Duration in Minutes", max_length=5)
    score_per_question = models.CharField(help_text="Enter Score per question", max_length=5)
    neg_score_per_question = models.CharField(help_text="Enter Negative Score per question", max_length=5, blank=True)
    test_start = models.DateTimeField(help_text="Enter Test Validity Start Date and time, leave blank if no constraint",
                                      blank=True)
    test_end = models.DateTimeField(help_text="Enter Test Validity End Date and time, leave blank if no expiry",
                                    blank=True)
    max_attempt = models.CharField(help_text="Maximum Attempts allowed, leave blank if no constraint", blank=True)

    def __str__(self):
        return self.test_num

    class Meta:
        ordering = ['test_num']





