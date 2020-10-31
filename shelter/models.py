from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=126)

    def __str__(self):
        return self.name


class Shelter(models.Model):
    address = models.CharField(max_length=126)
    company = models.CharField(max_length=126)
    leader = models.CharField(max_length=126)

    def __str__(self):
        return f"{self.address} @{self.company}"

    def from_dict(row):
        shelter = Shelter.objects.filter(address=row['shelter__address']).first()
        if shelter is None:
            shelter = Shelter()

        company = Company.objects.filter(name=row['shelter__company']).first()
        if company is None:
            Company.objects.create(name=row['shelter__company'])
            
        shelter.address = row['shelter__address']
        shelter.company = row['shelter__company']
        shelter.leader = row['shelter__leader']
        shelter.save()

        return shelter


class ShelterStaff(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    name = models.CharField(max_length=31)

    def __str__(self):
        return self.name

    def from_dict(row):
        shelter = Shelter.from_dict(row)

        staff = ShelterStaff.objects.filter(
            shelter=shelter, name=row['animal_schelter__responsible']).first()

        if staff is None:
            staff = ShelterStaff()

        staff.shelter = shelter
        staff.name = row['animal_schelter__responsible']

        staff.save()

        return staff
