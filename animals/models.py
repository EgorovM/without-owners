from datetime import datetime

from django.db import models

from options.models import *
from shelter.models import Shelter, ShelterStaff


def parse_str_to_date(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return date

    except:
        pass


class Animal(models.Model):
    KINDS = (
        ('dog', 'Собака'),
        ('cat', 'Кошка'),
    )

    SEXS = (
        ('male', 'Мужской'),
        ('female', 'Женский')
    )

    TAILS = [
        ('1', 'Обычный'),
        ('2', 'Саблевидный'),
        ('3', 'Купированный'),
        ('4', 'Крючком'),
        ('5', 'Прутом'),
        ('6', 'Поленом')
    ]

    BREEDS = [
        ('1', 'Метис'),
        ('2', 'Алабай')
    ]

    COLORS = [
        ('1', 'чепрачный'),
        ('2', 'светло-коричневый'),
        ('3', 'черный'),
        ('4', 'черно-белый'),
        ('5', 'биколор'),
        ('6', 'рыжий'),
        ('7', 'тигровый'),
        ('8', 'белый'),
        ('9', 'триколор'),
        ('10', 'темно-коричневый'),
        ('11', 'палевый'),
        ('12', 'кремовый'),
        ('13', 'серебристый'),
        ('14', 'перец с солью'),
        ('15', 'черный с белым'),
        ('16', 'красный'),
        ('17', 'черепаховый'),
        ('18', 'соболиный'),
        ('19', 'голубой с белым'),
        ('20', 'шоколадный'),
        ('21', 'дымчатый'),
        ('22', 'золотой'),
        ('23', 'арлекин'),
        ('24', 'фавн (бежевый)'),
        ('25', 'черно-красный-белый'),
        ('26', 'красный с белым'),
        ('27', 'абркосовый'),
        ('28', 'мраморный'),
        ('29', 'голубо-кремовый черепаховый')
    ]

    WOOLS = [
        ('1', 'Короткая'),
        ('2', 'Обычная'),
        ('3', 'Длинная'),
        ('4', 'Гладкая')
    ]

    EARS = [
        ('1', 'Стоячие'),
        ('2', 'Полустоячие'),
        ('3', 'Висячие'),
        ('4', 'Купированные')
    ]

    SIZES = [
        ('1', 'Средний'),
        ('2', 'Малый'),
        ('3', 'Крупный'),
        ('4', 'Большой')
    ]


    identification_number = models.CharField(max_length=126)
    cart_number = models.CharField(max_length=126)
    kind = models.ForeignKey(AnimalKind, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.FloatField()
    name = models.CharField(max_length=126)
    sex = models.ForeignKey(AnimalSex, on_delete=models.CASCADE)
    breed = models.ForeignKey(AnimalBreed, on_delete=models.CASCADE)
    color = models.ForeignKey(AnimalColor, on_delete=models.CASCADE)
    wool = models.ForeignKey(AnimalWool, on_delete=models.CASCADE)
    ears = models.ForeignKey(AnimalEars, on_delete=models.CASCADE)
    tail = models.ForeignKey(AnimalTail, on_delete=models.CASCADE)
    size = models.CharField(max_length=1, choices=SIZES)

    special_signs = models.TextField()
    is_socialization = models.BooleanField(default=False)

    sterialization_status = models.CharField(max_length=127)

    def __str__(self):
        return f"{self.identification_number} @{self.name}"

    @property
    def image(self):
        return self.asd

    def from_dict(row):
        animal = Animal.objects.filter(
            identification_number=row['animal__identification_number']).first()

        if animal is None:
            animal = Animal()

        keys = [key for key in row.keys() if key.split('__')[0] == 'animal']

        for col in keys:
            field, val = col.split('__')[1], row[col]
            setattr(animal, field, val)

        animal.save()

        return animal


class AnimalVacine(models.Model):
    VACINES = [
        ('1', 'Нобивак Трикат Трио Леоминор'),
        ('2', 'Nobivac Tricat Trio+R'),
        ('3', 'Нобивак Трикат Трио'),
        ('4', 'Астерион DHPPi-L'),
        ('5', 'Нобивак Трикат'),
        ('6', 'Пуревакс FelV'),
        ('7', 'Нобивак DHPPI'),
        ('8', 'Нобивак Lepto'),
        ('9', 'Мультикан-6'),
        ('10', 'Мультифел-4'),
        ('11', 'Мультикан-4'),
        ('12', 'Мультикан-8'),
        ('13', 'Мультикан-9'),
        ('14', 'Бешенство'),
        ('15', 'Мультикан'),
        ('17', 'Леоминор'),
        ('18', 'Астерион'),
        ('19', 'Рабикан'),
        ('20', 'Нобивак'),
        ('21', 'Lepto')]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    name = models.CharField(max_length=2, choices=VACINES)
    series = models.CharField(max_length=31)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} @{self.animal}"

    def from_dict(row):
        animal = Animal.from_dict(row)

        numbers = eval(row['animal_vacine__numbers'])
        if numbers[0] == 'nan':
            return

        dates = eval(row['animal_vacine__dates'])
        names = eval(row['animal_vacine__names'])
        series = eval(row['animal_vacine__series'])

        for number, date, name, series in zip(numbers, dates, names, series):
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

            vacine = AnimalVacine.objects.filter(
                animal=animal, date=date, name=name).first()

            if vacine is None:
                vacine = AnimalVacine()

            vacine.animal = animal
            vacine.name = name
            vacine.series = series if not series == 'nan' else ''
            vacine.date = date
            vacine.save()


class AnimalDrug(models.Model):
    DRUGS = [
        ('1', 'Паразицид-суспензия'),
        ('2', 'Дана СПОТ-ОН/Алевит'),
        ('3', 'Инспектор Тотал К'),
        ('4', 'Блох нэт/ альвет'),
        ('5', 'Каниквантел Барс'),
        ('6', 'Барс для кошек'),
        ('7', 'Рольф клуб 3D'),
        ('8', 'Стронгхолд'),
        ('9', 'Рольф Клуб'),
        ('10', 'Стронхолд'),
        ('11', 'Инсектал'),
        ('12', 'Празител'),
        ('13', 'Азинокс'),
        ('14', 'Тронцил'),
        ('15', 'Дронтал'),
        ('16', 'Прател'),
        ('17', 'БАРС')
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    name = models.CharField(max_length=2, choices=DRUGS)
    dose = models.CharField(max_length=31)
    date = models.DateField()

    def __str__(self):
        return f"{dict(self.DRUGS)[self.name]} @{self.animal}"

    def from_dict(row):
        animal = Animal.from_dict(row)

        numbers = eval(row['animal_drug__numbers'])
        dates = eval(row['animal_drug__dates'])
        names = eval(row['animal_drug__names'])
        doses = eval(row['animal_drug__doses'])

        for number, date, name, dose in zip(numbers, dates, names, doses):
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

            drug = AnimalDrug.objects.filter(
                animal=animal, date=date, name=name).first()

            if drug is None:
                drug = AnimalDrug()

            drug.animal = animal
            drug.name = name
            drug.dose = dose
            drug.date = date

            drug.save()


class AnimalCapture(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    district = models.CharField(max_length=127)
    address = models.CharField(max_length=127)
    act = models.CharField(max_length=31)

    certificater = models.CharField(max_length=127)
    certificater_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.act} @{self.animal}'

    def from_dict(row):
        animal = Animal.from_dict(row)

        capture = AnimalCapture.objects.filter(
            animal=animal,
            act=row['animal_capture__act']).first()

        if capture is None:
            capture = AnimalCapture()

        animal = Animal.from_dict(row)

        capture.animal = animal
        capture.certificater_date = parse_str_to_date(row['animal_capture__certificater_date'])

        for field in ['district', 'address', 'act', 'certificater']:
            setattr(capture, field, row['animal_capture__' + field])

        capture.save()

        return capture


class AnimalInspection(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    anamnes = models.CharField(max_length=127)
    date = models.DateField(blank=True)

    def __str__(self):
        return f"{self.anamnes} @{self.animal}"

    def from_dict(row):
        animal = Animal.from_dict(row)
        date = parse_str_to_date(row['animal_inspection__date'])

        inspection = AnimalInspection.objects.filter(
            animal=animal,
            date=date).first()

        if inspection is None:
            inspection = AnimalInspection()

        inspection.animal = animal
        inspection.date = date
        inspection.anamnes = row['animal_inspection__anamnes']
        inspection.save()

        return inspection


class AnimalInShelter(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)

    aviary_number = models.CharField(max_length=31)
    arrived_act = models.CharField(max_length=127)
    arrived_date = models.DateField()

    leave_act = models.CharField(max_length=127, blank=True)
    leave_reason = models.CharField(max_length=127, blank=True)
    leave_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.shelter} @{self.animal}"

    @property
    def image(self):
        return f"{shelter.address}/{animal.cart_number}.jpg"

    def from_dict(row):
        animal = Animal.from_dict(row)
        shelter = Shelter.from_dict(row)

        a_shelter = AnimalInShelter.objects.filter(
            animal=animal, shelter=shelter,
            arrived_act=row['animal_shelter__arrived_act']).first()

        if a_shelter is None:
            a_shelter = AnimalInShelter()

        arrived_date = parse_str_to_date(row['animal_shelter__arrived_date'])
        leave_date = parse_str_to_date(row['animal_shelter__leave_date'])

        a_shelter.arrived_date = arrived_date
        a_shelter.leave_date = leave_date

        a_shelter.animal = animal; a_shelter.shelter = shelter;
        a_shelter.aviary_number = row['animal_shelter__aviary_number']
        a_shelter.arrived_act = row['animal_shelter__arrived_act']
        a_shelter.leave_act = row['animal_shelter__leave_act']
        a_shelter.leave_reason = row['animal_shelter__leave_reason']
        a_shelter.save()

        return a_shelter
