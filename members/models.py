from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Member(User):
    clubs = models.ManyToManyField(Club)


class Club(models.Model):
    name = models.CharField(max_length=50, unique=False)
    club_admin = models.ForeignKey(Member, on_delete=models.DO_NOTHING)

