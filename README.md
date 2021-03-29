# REST API "Сласти от всех напастей"
Сервис, который позволяет нанимать курьеров на работу, принимать заказы и оптимально распределять заказы между курьерами, считая их рейтинг и заработок.
## Краткое описание обработчиков REST API
### POST /couriers
Принимает на вход в формате `json` список с данными о курьерах и графиком их работы. Курьеры работают только в заранее определенных районах, 
а так же различаются по типу: пеший, велокурьер и курьер на автомобиле. От типа курьера зависит его грузоподъемность — 10 кг, 15 кг и 50 кг соответственно.
Районы задаются целыми положительными числами. График работы задается списком строк формата `HH:MM-HH:MM`.

### PATCH /couriers/$courier_id
Позволяет изменить информацию о курьере. Принимает `json` и любые поля из списка: `courier_type`, `regions`,
`working_hours`.

### POST /orders
Принимает на вход в формате `json` список с данными о заказах. Заказы характеризуются весом, районом и
временем доставки.

### POST /orders/assign
Принимает id курьера и назначает максимальное количество заказов, подходящих по весу, району и графику работы.
Обработчик должен быть идемпотентным. Заказы, выданные одному курьеру, не должны быть доступны для выдачи другому.

### POST /orders/complete
Принимает 3 параметра: id курьера, id заказа и время выполнения заказа, отмечает заказ выполненным.

### GET /couriers/$courier_id
Возвращает информацию о курьере и дополнительную статистику: рейтинг и заработок.

## Используемые технологии
* Python 3.8.1
* PostgreSQL 12.6
* Flask 1.1.2
* Flask-SQLAlchemy 2.5.1
* Marshmallow 3.10.0
* PyTest 6.2.2
* Gunicorn 20.1.0
* Nginx 1.18.0

## Настройка сервера и установка
### Установка пакетов
1. Необохдимо выполнить установку `python3`, `virtualenv`, `postgresql`, `nginx` и всех пакетов, необходимых для их корректной работы.
```console
sudo apt install git htop python3-pip python3-dev python3-virtualenv postgresql postgresql-contrib libpq-dev nginx curl
```
2. Обновим `pip`:
```console
python3 -m pip install --upgrade pip
```
### Настройка PostgreSQL
1. Для начала сменим пароль:
```console
sudo passwd postgres
```
2. Затем создадим папку для нашего проекта:
```console
mkdir webservice
cd webservice/
```
3. Создадим новый ssh-ключ для GitHub репозитория.<br/>
Затем небходимо зайти в настройке на GitHub и добавить, сгенерированный ключ.
```console
ssh-keygen
cat ~/.ssh/id_rsa.pub
```
4. Клонируем репозиторий:
```console
git clone git@github.com:ivan-sidorov/DeliveryService.git
```
5. Переходим в директорию с проектом:
```console
cd DeliveryService/
```
6. Теперь необходимо создать виртуальное окружение и активировать его.
```console
virtualenv venv
source venv/bin/activate
```
7. Устанавливаем всенеобходимые модули из `requirements.txt`:
```console
pip install -r requirements.txt
```
8. **Теперь непосредственно переходим к настройке PostgreSQL:**
* Запускаем `psql`:
```console
sudo -u postgres psql
```
* Создаем пользователя, через которого мы будем взаимодействовать с базами. Так же создаем две БД — основная и для тестирования.
```
CREATE DATABASE deliveryservice;
CREATE USER username WITH PASSWORD 'password';
ALTER ROLE username SET client_encoding TO 'utf8';
ALTER ROLE username SET default_transaction_isolation to 'read committed';
ALTER ROLE username SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE deliveryservice to username;
CREATE DATABASE testviews;
GRANT ALL PRIVILEGES ON DATABASE testviews to username;
```
* Выходим из `psql`:
```
\q
```
* Теперь необходимо внести изменения в `~/webservice/DeliveryService/config.py`. Перед этим необходимо сгенерировать `SECRET_KEY`
```console
sudo nano config.py
```

```python
class Config(object):
    # SECRET_KEY = 'write here your secret key.'
    SQLALCHEMY_DATABASE_URI = 'postgresql://deliveryadmin:password@localhost:5432/deliveryservice'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
```
Также вносим изменения в `~/webservice/DeliveryService/Tests/test_app.py`:
```console
cd Tests/
sudo nano test_app.py
```
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://deliveryadmin:password@localhost:5432/testviews'
```
* Теперь необходимо удалить старую директорию с миграциями и создать новую:
```console
cd ..
rm -r migrations
flask db init
flask db migrate
flask db upgrade
```
### Настройка Gunicorn
1. Установка:
```console
pip install wheel
pip install gunicorn
```
2. Редактируем точку входа WSGI. На данный момент файл, который служит точкой входа в приложение имеет название `delivery.py`. Переименуем его в `wsgi.py` для удобства:
```console
mv delivery.py wsgi.py
```
3. Убедимся, что `Gunicorn` работает корректно:
```console
gunicorn --bind 0.0.0.0:8080 wsgi:app
```
4. Если вознилка такая ошибка, то попробуйте остановить `nginx`, если вдруг до этого вы его запускали.
```
[2021-03-29 16:13:10 +0000] [13577] [INFO] Starting gunicorn 20.1.0
[2021-03-29 16:13:10 +0000] [13577] [ERROR] Connection in use: ('0.0.0.0', 8080)
[2021-03-29 16:13:10 +0000] [13577] [ERROR] Retrying in 1 second.
[2021-03-29 16:13:11 +0000] [13577] [ERROR] Connection in use: ('0.0.0.0', 8080)
[2021-03-29 16:13:11 +0000] [13577] [ERROR] Retrying in 1 second.
[2021-03-29 16:13:12 +0000] [13577] [ERROR] Connection in use: ('0.0.0.0', 8080)
```
5. Работа с виртуальной средой закончена. Деактвируем ее:
```console
deactivate
```
6. Создаем `socket` файл и добавляем:  
```console
sudo nano /etc/systemd/system/deliveryservice.socket
```
```
[Unit]
Description=gunicorn socket
[Socket]
ListenStream=/run/deliveryservice.sock
[Install]
WantedBy=sockets.target
```
7. Создаем `service` файл и добавляем:
```console
sudo nano /etc/systemd/system/deliveryservice.service
```
```
[Unit]
Description=Gunicorn instance to serve deliveryservice
After=network.target

[Service]
User=entrant
Group=www-data
WorkingDirectory=/home/entrant/webservice/DeliveryService
Environment="PATH=/home/entrant/webservice/DeliveryService/venv/bin"
ExecStart=/home/entrant/webservice/DeliveryService/venv/bin/gunicorn --workers 9 --bind unix:deliveryse>


[Install]
WantedBy=multi-user.target
```
8. Запускаем `socket`:
```console
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

```
9. Проверим все ли правильно настроено:
```console
sudo systemctl status deliveryservice.socket
```
### Настройка nginx
1. Откроем серверный блок с конфигурацией по умолчанию. Нам не нужно создавать новый файл с расширением `.service`, так как у нас всего одно приложение, для которого
можно использовать `default`:
```console
sudo nano /etc/nginx/sites-available/default
```
```
server {
        listen 8080;
        listen [::]:8080;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                include proxy_params;
                proxy_pass http://unix:/run/deliveryservice.sock;
        }
}
```
2. Перезапустим, чтобы nginx применил изменения:
```console
sudo service nginx restart
```
3. Вновь проверим все ли хорошо:
```console
sudo systemctl status gunicorn
```
## Тестирование
1. Для того чтобы провести тестирование необходимо снова активировать виртуальную среду:
```console
source venv/bin/activate
```
2. Переходим в директорию с тестами:
```console
cd Tests/
```
3. Запускаем тестирование:
```console
pytest test_app.py
```
4. Если нужно больше подробностей, то:
```console
pytest -v test_app.py
```
