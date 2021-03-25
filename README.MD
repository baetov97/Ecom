# Ecom

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/baetov97/Ecom
$ cd Ecom
```

Install RabbitMQ for Celery(For tasks)

```sh
$ sudo apt install rabbitmq-server
$ systemctl is-enabled rabbitmq-server.service 
$ systemctl enable rabbitmq-server

```

Create .env file in the directory of project

    DJANGO_SECRET_KEY = ''
    
    #DB PSQL
    DB = ""
    DB_USER = ""
    DB_PASSWORD = ""
    DB_HOST=""
    DB_PORT=""
    
    
    EMAIL_USE_TLS = True
    EMAIL_HOST = ''
    EMAIL_PORT = 587
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''

git

```sh
$ git add . 
$ git pull origin master
$ git commit -m "some commit"
$ git push origin master
$ git rm -r --cached .
```

Database

```sh
$ CREATE DATABASE myproject;
$ CREATE USER myprojectuser WITH PASSWORD 'password';
$ ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
$ ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
$ ALTER ROLE myprojectuser SET timezone TO 'UTC';
$ GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
```

PIPENV install all packages

```sh
$ pipenv install
$ pipenv shell
```

Django

```shell
$ python manage.py makemigrations
$ python manage.py migrate
$ python managen.py test
```

Celery

```shell
$ celery -A ecommerce worker -l INFO
$ celery -A ecommerce beat
```

    