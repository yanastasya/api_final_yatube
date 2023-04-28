[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)

## Описание проекта:

Перед  вами REST API для проекта Yatube. Через этот интерфейс смогут работать мобильное приложение или чат-бот; через него же можно будет передавать данные в любое приложение или на фронтенд.

Yatube - это социальная сеть блогеров и их личных дневников с возможностью публиковать свои посты и просматривать, комментировать чужие, объединяться в сообщества, подписываться на избранных авторов. 


## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/yanastasya/api_final_yatube.git

```

```
cd yatube_api
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/scripts/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Примеры запросов:

### Эндпоинт http://127.0.0.1:8000/api/v1/posts/:

#### GET запрос:
Вы получите список всех публикаций. 
При указании параметров limit и offset выдача будет работать с пагинацией.
Например, для вывода по 5 публикаций на странице и получения второй страницы списка публикаций:
```
http://127.0.0.1:8000/api/v1/posts/?limit=5&offset=2
```

Вы получите ответ вида:

```
{
"count": n,
"next": "http://127.0.0.1:8000/api/v1/posts/?offset=3&limit=5",
"previous": "http://127.0.0.1:8000/api/v1/posts/?offset=1&limit=5",
"results": [
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
},
...
]
```
#### POST запрос:
Добавление новой публикации в коллекцию публикаций. Только для авторизованных пользователей.
В теле запроса обязательно передаётся текст поста (параметр text), возможно добавить картинку в двоичном формате (image) и id сообщества, к которому относится пост.

```
{
  "text": "string",
  "image": "string",
  "group": 0
}
```

Подробнее о возможностях API смотрите в документации.
