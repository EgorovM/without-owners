import pandas as pd

from django.shortcuts import render
from django.http import JsonResponse

from animals.models import (Animal, AnimalInspection, AnimalCapture,
                           AnimalDrug, AnimalVacine, AnimalInShelter)

from shelter.models import Shelter, ShelterStaff

def refresh_from_csv(request):
    df = pd.read_csv('animal_data_set.csv', sep=';')

    for row in df.iloc:
        animal = Animal.from_dict(row)
        animal_inspection = AnimalInspection.from_dict(row)
        animal_capture = AnimalCapture.from_dict(row)
        AnimalDrug.from_dict(row)
        AnimalVacine.from_dict(row)
        shelter = Shelter.from_dict(row)
        shelter_staff = ShelterStaff.from_dict(row)

        AnimalInShelter.from_dict(row)

    return JsonResponse({'error': 0})
