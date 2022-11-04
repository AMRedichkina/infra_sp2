# API_YAMDB #INFRA_SP2

# O проекте

- API_YAMDB создан для доступа сторонних приложений к проекту YAMDB(**REST API, DRF**).
API_YAMDB  позволяет выполнять запросы для взаимодействия с базой данных с разграниченим прав в зависимости от роли пользователя (супервользователь, администратор, модератор, пользователь).
-  Часть GET-запросов возможна без авторизации. Авторизация происсходит по JWT-токену.
С **API документацией** (подключен **Swagger**) можно ознакомиться по даресу: http://localhost/redoc/ после запуска проекта. 
- Со структурой БД можно ознакомиться по ссылке: https://dbdiagram.io/embed/62f224aac2d9cf52fa715ea5.
- Проект "упакован" в контейнеры: db, nginx, web. Для управления взаимодействием нескольких контейнеров применена утилита **docker-compose**.
- В проекте предусмотрена management-команда **load_data** для загрузки файлов в формате **csv** в БД через Django ORM. 
Инструкция по загрузке файлов описана после раздела с примерами запросов.

**Технологии:**

 - Python 3.7
 - Django 2.2.16
 - Django REST framework 3.12.4
 - Simple JWT 4.7.1
 - PostgreSQL
 - Docker
 - nginx
 - gunicorn

# Шаблон наполнения .env файла
Все секретные ключи помещаем в файл .env по адресу: api_yambd/infra/.env
Шаблон:
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
SECRET_KEY = 'p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##"l9()s'

# Oписание команд для запуска приложения в контейнерах

1) Клонировать репозиторий, добавить файл .env, подготовиться к созданию контейнера
```
git clone git@github.com:AMRedichkina/infra_sp2.git
cd infra_sp2/infra
touch .env 
```
2) Все секретные ключи помещаем в файл .env по адресу: api_yambd/infra/.env. Шаблон наполнения .env файла:

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
SECRET_KEY = 'p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##"l9()s'
```
2) Запускаем docker-compose
```
docker-compose build
```
Будут созданы и запущены в фоновом режиме необходимые для работы приложения контейнеры (db, web, nginx).

3) Затем нужно внутри контейнера web выполнить миграции, создать суперпользователя и собрать статику:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```
4) После этого проект должен быть доступен по адресу http://localhost/.

# Заполнение БД
**Вариант 1:**
Нужно зайти на на http://localhost/admin/, авторизоваться и внести записи в базу данных через админку.

Резервную копию базы данных можно создать командой
```
docker-compose exec web python manage.py dumpdata > fixtures.json 
```
**Вариант 2 (Загрузка в базу данных сведений из файлов CSV через Django ORM):**

*Набор необходимых файлов*

Для загрузки данных в БД вам необходимо, сгрупировать в директории файлы со следующими именами:

- category.csv (данные о категориях)
- genre.csv (данные о жанрах)
- titles.csv (данные о произведениях)
- users.csv (данные о пользователях)
- genre_title.csv (данные о связи произведения и его жанра)
- review.csv (данные об отзывах)
- comments.csv (данные о комментариях)

## Требования к полям файлов
Ниже вы найдёте минимальный набор полей необходимый в каждом файле чтобы загрузка прошла успешно.

#### * **category.csv** *(данные о категориях)*
| *id*        | *name*          | *slug* |
|:----------:|:-------------:| :-----:|
| 1      | Фильм | film |
| 2      | Книга | book |

#### * **genre.csv** *(данные о жанрах)*
| *id*        | *name*           | *slug* |
| :-------------: |:-------------:|:-----:|
| 1      | Драма | drama |
| 2      | Комедия | comedy |

#### * **titles.csv** *(данные о произведениях)*
| *id*  | *name*          | *year* | *category_id* | *description* |
|:---:|:-------------:|:-----:|:-----:|:-----:|
| 1   | Колобок | 1873 | 2 | A ball of bread |
| 2   | Назад в будущее | 1985 | 1 |  |

#### * **users.csv** *(данные о пользователях)*
| *id*  | *username*          | *email* | *role* | *first_name* | *last_name* | 
|:---:|:-------------:|:-----:|:-----:|:-----:|:-------|
| 100   | spider | sppitpark@aveng.com | user | Piter | Parker  |
| 101   | VolanDeMort | slizerin@hogwarts.com | admin |  |     |

#### * **genre_title.csv** *(данные о связи произведения и его жанра)*
| *id*        | *title_id*          | *genre_id* |
|:----------:|:-------------:| :-----:|
| 1      | 1 | 1 |
| 2      | 2 | 1 |

#### * **review.csv** *(данные об отзывах)*
| *id*  | *title_id*          | *text* | *author_id* | *score* | *pub_date* | 
|:---:|:-------------:|:-----:|:-----:|:-----:|:-------:|
| 1   | 1 | This was amazing | 100| 10 | 2019-09-24T21:08:21.567Z  |
| 2   | 1 | Avada Kedavra | 101 | 1 |  2019-09-24T21:08:21.567Z   |

#### * **comments.csv** *(данные о комментариях)*
| *id*  | *review_id*          | *text* | *author_id* | *pub_date* | 
|:---:|:-------------:|:-----:|:-----:|:-------:|
| 1   | 1 | Bullshit | 70 |2019-09-24T21:08:21.567Z  |
| 2   | 6 | Lumus | 60 |2019-09-24T21:08:21.567Z   |

## Загрузка данных

Загрузить данные можно используя команду

```shell
python3 manage.py load_data
```

*Комментарий: в передаваемых данных есть связанны поля. Будьте внимательны, рекомендуем предварительно ознакомиться со структурой БД*

## Авторы проекта:
- Лисицын Вячеслав
- Редичкина Александра