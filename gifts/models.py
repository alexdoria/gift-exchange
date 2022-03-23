from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
class Gift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ManyToManyField(Group)
    short_name = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    link = models.URLField(blank=True)

    def __str__(self):
        return f'{self.short_name} by {self.user.username}'
