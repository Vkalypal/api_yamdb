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

### Список часто используемых адресов

- [Главная страница проекта](http://127.0.0.1:8000/)

- [Административная панель](http://127.0.0.1:8000/admin/)

- [Документация проекта на OpenAPI/Swagger Redoc](http://127.0.0.1:8000/redoc/)

## Поддерживаемые запросы

| Method | Endpoint                                                             |
| ------ | -------------------------------------------------------------------- |
| POST   | /api/v1/auth/signup/                                                 |
| POST   | /api/v1/auth/token/                                                  |
|        |                                                                      |
| GET    | /api/v1/categories/                                                  |
| POST   | /api/v1/categories/                                                  |
| DELETE | /api/v1/categories/{slug}/                                           |
|        |                                                                      |
| GET    | /api/v1/genres/                                                      |
| POST   | /api/v1/genres/                                                      |
| DELETE | /api/v1/genres/{slug}/                                               |
|        |                                                                      |
| POST   | /api/v1/titles/                                                      |
| GET    | /api/v1/titles/{titles_id}/                                          |
| PATCH  | /api/v1/titles/{titles_id}/                                          |
| DELETE | /api/v1/titles/{titles_id}/                                          |
|        |                                                                      |
| GET    | /api/v1/titles/{title_id}/reviews/                                   |
| POST   | /api/v1/titles/{title_id}/reviews/                                   |
| GET    | /api/v1/titles/{title_id}/reviews/{review_id}/                       |
| PATCH  | /api/v1/titles/{title_id}/reviews/{review_id}/                       |
| DELETE | /api/v1/titles/{title_id}/reviews/{review_id}/                       |
|        |                                                                      |
| GET    | /api/v1/titles/{title_id}/reviews/{review_id}/comments/              |
| POST   | /api/v1/titles/{title_id}/reviews/{review_id}/comments/              |
| GET    | /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ |
| PATCH  | /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ |
| DELETE | /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ |
|        |                                                                      |
| GET    | /api/v1/users/                                                       |
| POST   | /api/v1/users/                                                       |
| GET    | /api/v1/users/{username}/                                            |
| PATCH  | /api/v1/users/{username}/                                            |
| DELETE | /api/v1/users/{username}/                                            |

## Авторы

- Алишер Ризабеков
- Никита Лётыч
- Михаил Логинов
