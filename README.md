# Проект на Django 3.

Данный проект на Django 3 является мега 

В проекте реализованны


## Список фильмов:

![alt text](images/block_scheme.png)

## Функционал



### Особенности:

> 
>
> 
>
> 
>
> 


## Вид интерфейса

![alt text](images/gui.png)

## Установка


Категории
Жанры
Фильмы
Кадры из фильма
Режиссеры\Актеры
Звезды рейтинга
Отзывы
Фильтры



docker network create -d bridge dj_m1_network
docker network ls

docker run -d --name pg_dj_zum -e POSTGRES_PASSWORD=postgres -p 0.0.0.0:15432:5432  postgres
#docker network connect dj_m1_network pg_dj_zum
docker network connect dj_m1_network pg_movies_20220824



docker build --tag zum/dj_m1:0.0.1 -f .dockerfile .
docker images 
docker run --name dj_zum --network=dj_m1_network -e DB_HOST=pg_movies_20220824  -p 0.0.0.0:8070:8001 zum/dj_m1:0.0.1



docker exec -it dj_zum python manage.py collectstatic --noinput
docker exec -it dj_zum bash

docker cp data/web_site/media dj_zum:/app/data/

