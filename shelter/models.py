from django.db import models


class Shelter(models.Model):

    shelter_address = models.CharField(max_length=126)
    company = models.CharField(max_length=126)
    leader = models.CharField(max_length=126)

    def __str__(self):
        return f"{self.company}"


class Shelter_staff(models.Model):
    name = models.CharField(max_length=31)

    def __str__(self):
        return self.name