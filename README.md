## RuSanit 
### Описание проекта

**Проект реализован на фреймворке Django. Реализованы такие функции как, 
добавление товара в корзину, формирование заказа, отправка заказа на доменную почту, 
отправка заявки на обратную связь**
#### Посетить сайт можно по [ссылке](https://rs-eco.ru/)
#
#### Для развертывания приложения на docker-контейнерах перейдите в ветку deploy
###
#### Локальное развертывание приложения:

```pip install -r requirements.txt```

В директории shop создайте папку migrations с файлом __init__.py внутри нее
#### Переименуйте файл .env.config в .env и заполните содержимое переменных окружения для корректного запуска приложения

###

#### Создание миграции репозитория

```python manage.py makemigrations```

```python manage.py migrate```

#### Регистрация в админке

```python manage.py createsuperuser```

#### Запуск приложения

```python manage.py runserver```