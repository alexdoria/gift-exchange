from django.db import models
from django.contrib.auth.models import User


def match_default():
    return {"from": "to"}


# Create your models here.
class Club(models.Model):
    name = models.CharField(max_length=50, unique=False)
    club_admin = models.ForeignKey('Member', null=True, on_delete=models.SET_NULL)

    match = models.JSONField(blank=True, default=match_default)

    def __str__(self):
        return f"{self.name}"

class Invitation(models.Model):
    invited_email = models.EmailField(max_length=50)
    invited_club = models.ForeignKey('Club', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.invited_email}"


class Member(models.Model):
    """Extends the default Django's User model"""
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    clubs = models.ManyToManyField(Club)
    invited_to = models.ManyToManyField(Club, related_name="invitations")

    def __str__(self):
        return f"{self.user.username}"