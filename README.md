Описание проекта electronics_network

electronics_network это django-rest-framework проект.

Данное серверное приложение создано для работы с базой данных по созданию, 
управлению сетью по продажам электроники.


Запуск проекта

Установить docker, выбрав соответствующую ОС: https://docs.docker.com/get-docker/

Клонировать в IDE проект https://github.com/igornastt/electronics_network на вашу локальную машину.

Запустить процесс создания и запуска образа приложения, с помощью команд:

docker-compose build docker-compose up

Изучить документацию проекта (swagger или redoc):

swagger http://127.0.0.1:8000/swagger/ redoc http://127.0.0.1:8000/redoc/

Открыть в браузере главную страницу проекта http://127.0.0.1:8000/ , и начать работу с эндпоинтами.


Приложения и модели

1. products

Product - модель продукта, производимого/закупаемого сетью и звеньями ее иерархии.

2. contacts

Contact - модель контакты и адрес ContactCityFilter - класс фильтр для админ-панели по полю City из модели Contact

3. factory

Factory - модель завода. 'Нулевая' модель, с т.з. закупок (у завода могут закупать товар объекты более низких по иерархии моделей). 

По полю MainNetwork связана с основной сетью и обязана ее иметь. 

Связана с Products (ManyToMany) Связана с Contact (OneToOneField)

4. networks_electronics

MainNetwork - модель основной сети (вершина иерархии сети). Остальные звенья сети связаны с моделью по ForeignKey.

RetailNetwork - модель розничная сеть. Обязательно имеет основную сеть (MainNetwork по FK). 

Связана с Product (ManyToMany) Связана с Contact (OneToOne) 

Может иметь завод-поставщик (связь по FK c Factory)MainNetwork - модель основной сети (вершина иерархии сети). Остальные звенья сети связаны с моделью по ForeignKey.

RetailNetwork - модель розничная сеть. Обязательно имеет основную сеть (MainNetwork по FK). Связана с Product (ManyToMany) Связана с Contact (OneToOne) 

Может иметь завод-поставщик (связь по FK c Factory)

5. sole_proprietor

SoleProprietor - модель индивидуальный предприниматель. Обязательно имеет основную сеть (MainNetwork по FK). 

Связана с Product (ManyToMany). Связана с Contact(OneToOne). Может иметь поставщика либо завод, либо розничную суть (связь по FK). Валидация на уровне модели (clean()).

6. users

User - кастомная модель пользователей.

Переопределен и кастомизирован также и UsersManager класс (./users/manager.py) Переопределен и кастомизировать admin interface. (./users/admin.py)

users/permissions.py

Имеется два permission класса: IsUserActive - доступ только для активных сотрудников IsStaffOrSuperuser - группа менеджеров

Есть validator:

EmailValidator для пользователей, почтовый адрес должен ссылаться на почтовый хостинг ".ru" или ".com"

Описаны unnitest


Пагинация

Для всех моделей реализована пагинация с выводом 10 объектов на страницу. Максимальное значение - 50 объектов на страницу.

Фильтрация

Для всех ListViews/endpoints всех моделей приложений (products, contacts, networks_electronics и sole_proprietor) реализована фильтрация по городу (contact_city). Фильтрация по городу добавлена и в admin interface.

Проведена проверка синтаксиса и соблюдения PEP с помощью flake8.

Эндпоинты и документация

Настроена документация yasg-drf. Все endpoints можно изучить по ссылкам:

http://localhost:8000/swagger/ http://localhost:8000/redoc/


Безопасность

Для проекта настроен CORS.

Все endpoints защищены IsAuthenticated permission на уровне проекта. 

На уровне views приложений отдельно добавлен кастомный IsUserActive permission.
