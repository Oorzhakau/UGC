# Проектная работа 9 спринта
![UGC workflow](https://github.com/Oorzhakau/ugc_sprint_2/workflows/UGC-workflow/badge.svg)

Ссылка на репозиторий:
https://github.com/Oorzhakau/ugc_sprint_2

## Описание проекта
Сервис UGC (ugc_app) регистрирует время просмотра фильма пользователем, его лайки (возможно оценка от 0 до 10),
рецензии, а также закладки для будущего просмотра.

## Технологии
* UGC API приложение - FastApi
* Хранилище данных - MongoDB
* Транзакционная система (OLTP) - Kafka
* Система интерактивной аналитической обработки (OLAP) - Clickhouse
* Система логгирования - ELK (Elasticsearch, Logstash, Kibana)
* Сборщик ошибок - Sentry
* Инфраструктура развертывается docker-compose

## Задания
* reseach/storage_research/research.ipynb - исследование по выбору хранилища данных по закладкам, лайкам и просмотрам

## Запуск проекта
1. Заполнить `.env` по шаблону `.env_example`. При debug проекта **auth_app**
в директории auth_app также заполнить `.env`
2. Выполнить команду для разворачивания контейнеров
```bash
sudo docker-compose up --build
```
3. Для debug запустите выполните команду:
```bash
sudo docker-compose -f docker-compose.dev.yml up --build
```
4. Запуск тестов (предварительно заполнить файл .env в папке ./tests/functional/)
```bash
cd tests/functional/ &&
sudo docker-compose up --build
```

При успешном запуске проекта можно перейти на документации API проектов
  * Сервис Auth `http://127.0.0.1/swagger/`
  * Сервис UGC `http://127.0.0.1/ugc/api/openapi`
  * Сервис трассера `http://127.0.0.1:16686/search`
  * Сервис kibana `http://127.0.0.1:5601/`

## Выбор OLAP хранилищ
Сравнение и выбор хранилища для аналитики приведено в `olap_research`. Для запуска окружения в ранее указанной
папке выполнить команду
```bash
docker-compose up --build
```
После запуска `jupyter` сервиса (в logs указан localhost:8888 с токеном), открыть `research.ipynb` ноутбук
и ознакомиться с выполненным исследованием.