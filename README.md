# Foodgram - diplom  
Дипломный проект - сайт для публикации рецептов, он позволяет смотреть и создавать рецепты, добавлять их в избранное, скачивать список продуктов для похода в магазин и подписываться на любимых авторов.  

адрес сервера - https://foodgramblog.myddns.me  
администратор: логин - a@a.ru, пароль - q  

Документация доступна по https://foodgramblog.myddns.me/api/docs/  

## Инструкция для локального запуска  

Сервер - http://localhost:8000/  

В корне проекта выполните команду  
```docker-compose -f docker-compose.yml up -d```  

Смотрим название контейнера backend  
```docker ps | grep backend```  

Заходим в контейнер backend  
```docker exec -it <имя котейнера backend> bash```  

Выполняем в нем миграции и создаем суперюзера  
```python3 manage.py migrate```  
```python3 manage.py createsuperuser```  

Собираем статику  
```python3 manage.py collectstatic```  

Копируем ее в папку backend_static  
```cp -r /app/collected_static/. /backend_static/static/ ```  

## Технологии  

```Python``` ```Django DRF``` ```PostgreSQL``` ```Docker``` ```Yandex Cloud``` ```CI``` ```CD```  

## Автор  
Беспалов Роман  
