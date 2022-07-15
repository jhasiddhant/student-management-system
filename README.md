# Student Management System

#

## Tech Stacks Used:
HTML, CSS, JavaScript, Django, MySQL
#

## Cloning the repository

--> Clone the repository using the command below :
```bash
git clone https://github.com/jhasiddhant/student-management-system.git
```

--> Move into the directory of the project files : 
```bash
cd student-management-system
```

--> Install the requirements :
```bash
pip install -r requirements.txt
```

#

## Creating MySQL Database:
step 1:
```python
create database sms;
```
step 2:
```python
create user 'sms'@'localhost' identified with mysql_native_password by 'password';
```
step 3:
```python
grant all privileges on *.* to 'sms'@'localhost';
```
#

## Connecting Database:
Delete all old migrations file in base/migrations and then run following commands:
```python
py manage.py makemigrations
```
```python
py manage.py migrate
```
#

## Running the App:
--> Before running we create superuser :
```bash
py manage.py createsuperuser
```

--> To run the App, we use :
```bash
py manage.py runserver
```

> ⚠ Then, the development server will be started at http://127.0.0.1:8000/

#

## App Preview:
