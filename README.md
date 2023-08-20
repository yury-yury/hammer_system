

# Реферальная система

## Тестовое задание для Python разработчика компании Hammer System

### Стек технологий

Данное тестовое задание выполнено с использованием следующего стека технологий:
    - Phyton 3
    - Django 4
    - Django REST Framework 3
    - PostgreSQL 
    - DRF-Spectacular + SwaggerUI

### Задание

Реализовать простую реферальную систему. Минимальный интерфейс для тестирования

Реализовать логику и API для следующего функционала :

-	Авторизация по номеру телефона. Первый запрос на ввод номера телефона. 
Имитировать отправку 4хзначного кода авторизации(задержку на сервере 1-2 сек). Второй запрос на ввод кода.

-	Если пользователь ранее не авторизовывался, то записать его в бд.

-	Запрос на профиль пользователя.

-	Пользователю нужно при первой авторизации нужно присвоить рандомно сгенерированный 
6-значный инвайт-код(цифры и символы).

-	В профиле у пользователя должна быть возможность ввести чужой инвайт-код(при вводе проверять на существование). 
В своем профиле можно активировать только 1 инвайт код, если пользователь уже когда-то активировал инвайт код, 
то нужно выводить его в соответсвующем поле в запросе на профиль пользователя.

-	В API профиля должен выводиться список пользователей(номеров телефона), 
которые ввели инвайт код текущего пользователя.

-	Реализовать и описать в readme Api для всего функционала.

-	Создать и прислать Postman коллекцию со всеми запросами.

### Запуск проекта

Для запуска проекта необходимо:

1. Создать базу данных для использования в приложении.

2. В корневой директории проекта создать файл .env в котором указать данные для доступа к серверу базы данных:

    - SECRET_KEY=django-insecure-j^$x87fw-d^5wii4(qiml#gnsqmua#s22y+bi(6jc_x14em^3o
    - DB_USER=
    - DB_PASSWORD=
    - DB_HOST=
    - DB_PORT=

3. Создать и активировать виртуальное окружение проекта.(опционально)

4. Установить зависимости используемые в проекте из файла requirements.txt(pip install -r requirements.txt)

5. Применить имеющиеся миграции к базе данных.(python3 manage.py migrate)

6. Запустить сервер (python3 manage.py runserver)

#### Примечание

* Коллекция запросов Postman coхранена в виде файла Referral system.postman_collection.json находящегося в корне проекта.
* По URL  адресу /api/schima/swagger-ui/ можно просмотреть документацию по реализованным методам API 
* При выполнении первого запроса на авторизацию четырехзначный цифровой код выводиться в консоль.


