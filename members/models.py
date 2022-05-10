from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Club(models.Model):
    name = models.CharField(max_length=50, unique=False)
    club_admin = models.ForeignKey('Member', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name} created by {self.club_admin}"


class Member(models.Model):
    """Extends the default Django's User model"""
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    clubs = models.ManyToManyField(Club)
    invited_to = models.ManyToManyField(Club, related_name="invitations")

    def __str__(self):
        return '{}'.format(self.user.username)
