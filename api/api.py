import random
import string
import base64
import datetime

import requests

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.http         import JsonResponse
from django.core.files.base import ContentFile
from django.shortcuts    import render

from animals.models import Animal

class Route:
    @csrf_exempt
    def route(request):
        route = Route()

        print(request.method)
        handle = getattr(route, "do_" + request.method)

        try:
            return handle(request)

        except Exception as e:
            print("EXCEPTION:", e)
            return route.raise_error(-1)

    def do_GET(self, request):
        section = request.GET.get('section', None)
        method  = request.GET.get('method',  None)
        params  = request.GET.get('params',  None)

        if section == None and method == None or params == None:
            return self.raise_error(1)

        attr = section + "_" + method

        if not hasattr(self, attr):
            print(hasattr(self, attr), attr)
            return self.raise_error(9)

        handle = getattr(self, attr)
        print('params:', params)

        return handle(eval(params))

    def do_POST(self, request):
        section = request.POST.get('section', None)
        method  = request.POST.get('method',  None)
        params  = request.POST.get('params',  None)

        if section == None and method == None or params == None:
            return self.raise_error(1)

        attr = section + "_" + method

        if not hasattr(self, attr):
            return self.raise_error(9)

        handle = getattr(self, attr)

        return handle(eval(params))

    def animal_filter(self, params):
        animals = Animal.filter_by_params(params, is_socialization=True)

        result = self.generate_result_objects(animals, 'animals')

        return self.json_response(result)

    def generate_result_one_object(self, object, fields=None):
        result = {}

        if fields is None:
            fields = object.__dict__

        for attr_name in fields:
            if attr_name[0] != "_":
                data, attr_name = self.get_object_attr(object, attr_name)

                result[attr_name] = data

        return dict([( type(object).__name__.lower(), result )])

    def get_object_attr(self, object, attr_name):
        data = getattr(object, attr_name)

        if attr_name.endswith('_id') and hasattr(object, attr_name[:-3]):
            attr_name = attr_name[:-3]

            if hasattr(getattr(object, attr_name), 'name'):
                data = getattr(getattr(object, attr_name), 'name')


        if type(data).__name__ == "method":
            data = data()
        elif type(data).__name__ == "ImageFieldFile":
            data = data.url
        elif type(data).__name__ == "datetime":
            data = str(data.now())

        return data, attr_name

    def generate_result_objects(self, objects, name, fields=None):
        result = []

        for object in objects:
            data = self.generate_result_one_object(object, fields=fields)
            result.append(data[type(object).__name__.lower()])

        return {
            'data': result,
            'count': len(result)
        }

    def generate_result_by_key_value(self, key, value):
        return {
            key: value,
        }

    def json_response(self, result=[], error_code=0):

        return JsonResponse({
            "result": result,
            "error_code": error_code,
            "error_text": self.ERRORS[error_code],
        })

    def raise_error(self, error_code, text=None):
        error_text =  self.ERRORS[error_code] if text is None else text
        print("error", error_text)
        return JsonResponse(
            {
                "result" : [],
                "error_code": error_code,
                "error_text": error_text
            }
        )

    ERRORS = {
        -1: 'Неожиданная ошибка.',
        0:  'Успешно!',
        1:  'Необходимые параметры отсутствуют',
        2:  'Неизвестный город',
        3:  'Неправльные имена полей',
        4:  'Нет поля: point',
        5:  'Неизвестная инициатива',
        6:  'Неправльный логин или пароль',
        7:  'Пользователь с таким телефоном уже существует',
        8:  'Неправльный код',
        9:  'Section или method не сущесвует',
        10: 'ф',
        11: 'Неизвестный section',
        12: 'Повторное голосование невозможно'
    }
