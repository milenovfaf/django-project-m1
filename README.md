# Проект на Django 3.


В проекте реализованны

## Список фильмов:

![alt text](images/block_scheme.png)

## Функционал
## Модели

> Категории
> Жанры
> Фильмы
> Кадры из фильма
> Режиссеры\Актеры
> Звезды рейтинга
> Отзывы
> Фильтры


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




## Сервер

ssh -p 13022 root@45.141.77.236
root@45.141.77.236:13022  формат для mc
https://zum.point900.com/


docker network create -d bridge dj_m1_network
docker network ls

docker run -d --name pg_dj_zum -e POSTGRES_PASSWORD=postgres  postgres
docker network connect dj_m1_network pg_dj_zum



docker build --tag zum/dj_m1:0.0.1 -f .dockerfile .
docker images 
docker run -d --restart=always  --name dj_zum -v /root/data/dj_m1/data:/app/data --network=dj_m1_network -e DB_HOST=pg_dj_zum  -p 0.0.0.0:80:8001 zum/dj_m1:0.0.1

# docker cp dj_zum:/app/data /root/data/dj_m1

docker exec -it dj_zum python manage.py collectstatic --noinput
docker exec -it dj_zum python manage.py migrate
docker exec -it dj_zum python manage.py createsuperuser
docker exec -it dj_zum bash


