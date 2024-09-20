import requests
import json

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        if amount <= 0:
            raise APIException("Количество должно быть больше нуля.")

        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        response = requests.get(url)

        if response.status_code != 200:
            raise APIException(f"Ошибка запроса к API: {response.status_code}")

        data = json.loads(response.content)
        if quote not in data['rates']:
            raise APIException(f"Валюта '{quote}' не найдена.")

        base_rate = data['rates'][quote]
        total_amount = base_rate * amount

        return round(total_amount, 4)