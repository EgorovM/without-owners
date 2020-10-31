from django.db import models


class Animal(models.Model):
    KINDS = (
        ('dog', 'Собака'),
        ('cat', 'Кошка'),
    )

    SEXS = (
        ('M', 'Мужской'),
        ('F', 'Женский')
    )

    identification_number = models.CharField(max_length=126)
    cart_number = models.CharField(max_length=126)
    kind = models.CharField(max_length=3, choices=KINDS)
    age = models.IntegerField()
    weight = models.FloatField()
    name = models.CharField(max_length=126)
    sex = models.CharField(max_length=3, choices=SEXS)
    breed = models.CharField(max_length=126)
    color = models.CharField(max_length=126)
    wool = models.CharField(max_length=126)
    ears = models.CharField(max_length=126)
    tail = models.CharField(max_length=126)
    size = models.CharField(max_length=126)
    special_signs = models.TextField()
    is_socialization = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.identification_number} @{self.name}"


class AnimalVacine(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    name = models.CharField(max_length=31)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} @{self.animal}"


class AnimalDrug(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    name = models.CharField(max_length=31)
    dose = models.CharField(max_length=31)
    date = models.DateField()

    def __str__(self):
        return f"{self.vacine_name} @{self.animal}"
