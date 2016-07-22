from django.db import models
from django.contrib.auth.models import User


class Compte(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return "Ceci est le compte de : " + str(self.user.username)
