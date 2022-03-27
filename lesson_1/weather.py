import requests
from pprint import pprint

# видоизменил начальную ссылку на эту https://api.openweathermap.org/data/2.5/weather?q=Paris&appid={API key}
# достал её от сюда https://openweathermap.org/current

# ссылка, которая идет до знака вопроса, потом идут параметры
url = 'https://api.openweathermap.org/data/2.5/weather'

# заношу параметры в переменные (название города и апи ключ, апи ключ взял от сюда https://home.openweathermap.org/api_keys)
city = 'Paris'
appid = 'def9a2cf8f063a7aa4cbe66da9bd625e'

# создаю словарь, в который передаю ранее заданные переменные
params = {
    'q': city,
    'appid': appid
}

# создаю запрос, в котором передаю ссылку и параметры, указанные выше
response = requests.get(url, params=params)

# преобразую стринговый результат в json объект
j_data = response.json()
# Выполнив команду ниже, вернется весь json (который тут будет словарем) со всеми данными, не все они нужны
#pprint(j_data)

# Вывожу только данные о температуре воздуха
print(f"В городе {j_data['name']} температура {round(j_data['main']['temp'] - 273.15)} градусов")

