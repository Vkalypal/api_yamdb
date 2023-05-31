# Проект "YaMDb"

## Описание

Проект **YaMDb** собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Установка

### Клонирование репозитория

```sh
git clone https://github.com/Vkalypal/api_yamdb.git
```

### Установка виртуального окружения

```sh
cd api_yamdb
python -m venv venv
```

### Активация виртуального окружения

- для OS Linux (MacOS)

```sh
source venv/bin/activate
```

- для OS Windows

```powershell
source venv/Scripts/activate
```

### Установка необходимых зависимостей

```sh
pip install -r requirements.txt
```

### Смена текущей директории

```sh
cd api_yamdb
```

### Создание базы данных

```sh
python3 manage.py makemigrations
python3 manage.py migrate
```

### Загрузка тестовых данных в базу данных (опционально)

```sh
python3 manage.py import_data
```

### Создание пользователя с правами администратора

```sh
python3 manage.py createsuperuser
```

### Запуск проекта

```sh
python manage.py runserver
```

## Список часто используемых адресов

- [Главная страница проекта](http://127.0.0.1:8000/)

- [Административная панель](http://127.0.0.1:8000/admin/)

- [Документация проекта на OpenAPI/Swagger Redoc](http://127.0.0.1:8000/redoc/)

## <a name="queries"></a> Поддерживаемые запросы

### POST /api/v1/auth/signup/

Получить код подтверждения на переданный email для регистрации нового пользователя
Права доступа: Доступно без токена.
Использовать имя 'me' в качестве username запрещено.
Поля email и username должны быть уникальными.

#### Формат ответа

```json
{
  "email": "string",
  "username": "string"
}
```

[Вернуться к списку запросов](#queries)

### POST /api/v1/auth/token/

Получение JWT-токена в обмен на username и confirmation code.

Права доступа: Доступно без токена.

#### Формат ответа

```json
{
  "token": "string"
}
```

[Вернуться к списку запросов](#queries)

### GET /api/v1/categories/

### GET /api/v1/categories/?search=slug

Получить список всех категорий

Права доступа: Доступно без токена

#### Формат ответа

```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

[Вернуться к списку запросов](#queries)

### POST /api/v1/categories/

Создать категорию.

Права доступа: Администратор.

Поле slug каждой категории должно быть уникальным.

#### Формат ответа

```json
{
  "name": "string",
  "slug": "string"
}
```

[Вернуться к списку запросов](#queries)

### DELETE /api/v1/categories/{slug}/

Удалить категорию.

Права доступа: Администратор.

#### Формат ответа

Status code 204
[Вернуться к списку запросов](#queries)

### GET /api/v1/genres/

### GET /api/v1/genres/?search=slug

Получить список всех жанров.

Права доступа: Доступно без токена

#### Формат ответа

```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

[Вернуться к списку запросов](#queries)

### POST /api/v1/genres/

Добавить жанр.

Права доступа: Администратор.

Поле slug каждого жанра должно быть уникальным.

#### Формат ответа

```json
{
  "name": "string",
  "slug": "string"
}
```

[Вернуться к списку запросов](#queries)

## DELETE /api/v1/genres/{slug}/

Удалить жанр.

Права доступа: Администратор.

#### Формат ответа

Status code 204
[Вернуться к списку запросов](#queries)

### POST /api/v1/titles/

Добавить новое произведение.

Права доступа: Администратор.

Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).

При добавлении нового произведения требуется указать уже существующие категорию и жанр.

#### Формат ответа

```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

[Вернуться к списку запросов](#queries)

### GET /api/v1/titles/{titles_id}/

Информация о произведении

Права доступа: Доступно без токена

#### Формат ответа

```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

[Вернуться к списку запросов](#queries)

### PATCH /api/v1/titles/{titles_id}/

Обновить информацию о произведении

Права доступа: Администратор

#### Формат ответа

```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

[Вернуться к списку запросов](#queries)

### DELETE /api/v1/titles/{titles_id}/

Удалить произведение.

Права доступа: Администратор.

#### Формат ответа

Status code 204
[Вернуться к списку запросов](#queries)

### GET /api/v1/titles/{title_id}/reviews/

Получить список всех отзывов.

Права доступа: Доступно без токена.

#### Формат ответа

```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```

[Вернуться к списку запросов](#queries)

### POST /api/v1/titles/{title_id}/reviews/

Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение.

Права доступа: Аутентифицированные пользователи.

#### Формат ответа

```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

[Вернуться к списку запросов](#queries)

### GET /api/v1/titles/{title_id}/reviews/{review_id}/

Получить отзыв по id для указанного произведения.

Права доступа: Доступно без токена.

#### Формат ответа

```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

[Вернуться к списку запросов](#queries)

### PATCH /api/v1/titles/{title_id}/reviews/{review_id}/

Частично обновить отзыв по id.

Права доступа: Автор отзыва, модератор или администратор.

#### Формат ответа

```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

[Вернуться к списку запросов](#queries)

### DELETE /api/v1/titles/{title_id}/reviews/{review_id}/

Удалить отзыв по id

Права доступа: Автор отзыва, модератор или администратор.

#### Формат ответа

Status code 204
[Вернуться к списку запросов](#queries)

### GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/

Получить список всех комментариев к отзыву по id

Права доступа: Доступно без токена.

#### Формат ответа

```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```

[Вернуться к списку запросов](#queries)

### POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/

Добавить новый комментарий для отзыва.

Права доступа: Аутентифицированные пользователи.

#### Формат ответа

```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

[Вернуться к списку запросов](#queries)

### GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

Получить комментарий для отзыва по id.

Права доступа: Доступно без токена.

#### Формат ответа

```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

[Вернуться к списку запросов](#queries)

### PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

Частично обновить комментарий к отзыву по id.

Права доступа: Автор комментария, модератор или администратор.

#### Формат ответа

```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

[Вернуться к списку запросов](#queries)

### DELETE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

Удалить комментарий к отзыву по id.

Права доступа: Автор комментария, модератор или администратор.

#### Формат ответа

Status code 204
[Вернуться к списку запросов](#queries)

### GET /api/v1/users/

Получить список всех пользователей.

Права доступа: Администратор

#### Формат ответа

```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```

[Вернуться к списку запросов](#queries)

### POST /api/v1/users/

Добавить нового пользователя.

Права доступа: Администратор

Поля email и username должны быть уникальными.

#### Формат ответа

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

[Вернуться к списку запросов](#queries)

### GET /api/v1/users/{username}/

Получить пользователя по username.

Права доступа: Администратор

#### Формат ответа

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

[Вернуться к списку запросов](#queries)

### PATCH /api/v1/users/{username}/

Изменить данные пользователя по username.

Права доступа: Администратор.

Поля email и username должны быть уникальными.

#### Формат ответа

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

[Вернуться к списку запросов](#queries)

### DELETE /api/v1/users/{username}/

Удалить пользователя по username.

Права доступа: Администратор.

#### Формат ответа

Status code 204
[Вернуться к списку запросов](#queries)

## Использованные технологии

- [Python - интерпретируемый язык программирования](https://www.python.org)

- [Django - свободный фреймворк для веб-приложений на языке Python](https://www.djangoproject.com)

- [Django REST framework - мощный и гибкий набор инструментов для создания Web API](https://www.django-rest-framework.org)

- [Simple JWT - дополнение, реализующее JSON Web Token аутентификацию для Django REST Framework](https://github.com/jazzband/djangorestframework-simplejwt)

- [Django-filter - приложение, реализующее фильтрацию наборов запросов](https://github.com/carltongibson/django-filter)

## Авторы

- Алишер Ризабеков
- Никита Лётыч
- Михаил Логинов
