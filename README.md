# FakeCSV

FakeCSV is a `Django` app to create CSV data sets of fake data of different types, such as full name, job, company name etc.

It was originally built for test challenge at `planeks.net`.

## How to build this app

- ### Navigate to the project root folder

- ### Optionally set up and activate the virtual environment:
```
virtualenv venv
source env/bin/activate
```

- ### Install the requirements:
```
pip install .
```
- ### Configure local Redis server (`redis://localhost:6379/0` is used) 

- ### Configure Celery worker (app name is `planeks_fakecsv`)


- ### Run migrations to create database infrastructure:
```
python manage.py migrate
```


- ### Run the project locally:
```
python manage.py runserver
```


## Now you should be able to access the web service and web application on the following addresses:

```
127.0.0.1:8000/
127.0.0.1:8000/auth
127.0.0.1:8000/create
127.0.0.1:8000/<int:schema_id>/edit
127.0.0.1:8000/<int:schema_id>/delete
127.0.0.1:8000/<int:schema_id>/datasets
```


### This app also can be found on [Heroku](https://planeks-fakecsv.herokuapp.com/)
