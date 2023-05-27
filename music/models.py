from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Song(models.Model):
    ACCESS_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('protected', 'Protected'),
    )

    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='songs/')
    access_type = models.CharField(max_length=10, choices=ACCESS_CHOICES)
    allowed_emails = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    


class MusicFile(models.Model):
    # Other fields

    access_emails = models.TextField(blank=True)

    def has_access(self, user):
        if self.access_emails:
            allowed_emails = [email.strip() for email in self.access_emails.split()]

            if user.email in allowed_emails:
                return True

        return False



