## Loan Management System

> Django, Djangorestframwork, Postgresql, Docker

## BACKEND

### Library Used

- Django
- djangorestframework
- psycopg2-binary
- djangorestframework-simplejwt

### Why choose Django and Postgresql (For Backend)?

**Django** is the one of the most popular web framework for python, Django takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. As for Postgresql it works well with Django and also preferable for the assignment as mentioned [here](./read.md).

### INSTALLATION && USAGE

No need to worry about installation, if docker and docker-compose is not installed in your system please install and follow along the step(s).

- Git Clone this repo and enter into the LMS directory.
- Create
    - a file 'backend-env' with content
        ```
        debug=<>
        secret_key=<>
        postgres=<>
        DB_HOST=<>
        DB_NAME=<>
        DB_USER=<>
        DB_PASS=<>
        DB_PORT=<>
        ```
        reffer this file [here](./backend-env-sample).
    - a file 'pgdb-env' with content
        ```
        POSTGRES_DB=<>
        POSTGRES_USER=<>
        POSTGRES_PASSWORD=<>
        ```
        reffer this file [here](./pgdb-env-sample).

- Run the command ` docker-compose up --build `. And it should be up and running. Checkout the endpoints mentioned below. Note test case and  will be run and created.
- To run test case, `docker-compose exec backend python manage.py test`. Note test case automatically run during execution of previous command ` docker-compose up --build `.
- To create admin user, `docker-compose exec backend python manage.py createsuperuser`.

### Admin Panel

Django provide built-in admin panel can be access from `localhost:8000/admin` url. If you used `docker-compose up --build` then admin user will be created by  `docker-compose exec backend python manage.py createsuperuser`. Otherwise create using `python manage.py createsuperuser`

### API ENDPOINTS

#### **BASE_URL**: /api/users

### To get Login

#### Request

`POST <BASE_URL>/login/`
<br />
Body: `{'email': 'user@mail.com', 'password':'passwd123'}`

#### Response

```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyNTI4NDIzMiwianRpIjoiMTQ0Y2E0MzkzZjNmNDM5NWI1MDhiM2VmNjA0MjUxYTIiLCJ1c2VyX2lkIjoiMmY4Mzc5NzMtNmYwOC00ZmYwLThkMTgtMTJmNzkxZDMwNTA0In0.iIm7aLCUyMCO9yvll00HRxIH5fAdlVD_5yeCKYEQIGw",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI3Nzg5ODMyLCJqdGkiOiJhNmM4MGM5Y2QzNTI0ZjQ3ODhjMmI0ZTE1OWVjOGZiZiIsInVzZXJfaWQiOiIyZjgzNzk3My02ZjA4LTRmZjAtOGQxOC0xMmY3OTFkMzA1MDQifQ.mEN1MwdGrYLRHharSoTzc3zbj8QEqlv1_H8-wWfVgdw",
    "id": "2f837973-6f08-4ff0-8d18-12f791d30504",
    "email": "customer2@mail.com",
    "username": "customer2",
    "user_type": "customer",
    "date_joined": "2021-06-27T15:26:04.635540Z",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI3Nzg5ODMyLCJqdGkiOiJkYTI3YTc0NzI3NDc0NmQ3ODAxNjE4OGY5ZDk1YmUyMCIsInVzZXJfaWQiOiIyZjgzNzk3My02ZjA4LTRmZjAtOGQxOC0xMmY3OTFkMzA1MDQifQ.hhz7n6W46mgVIBAWLIu3zMd-XolT7VRZjaCZPclDwHQ"
}
```

### To get register agent

#### Request

`POST <BASE_URL>/register/agent/`
<br />
Body: `{
    "username":"agent_1",
    "email":"agent_1@mail.com",
    "password":"agent_1"
}`

#### Response

```json
{
    "id": "fca6b3b4-2645-4852-948a-7f51efd1dc87",
    "email": "agent_1@mail.com",
    "username": "agent_1",
    "user_type": "agent",
    "date_joined": "2021-06-29T17:21:48.585464Z",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI3NTc5MzA5LCJqdGkiOiI5ZGY4NDkzMGE3ZGI0YzZhYjg2MTVlZGM3MmY3ZmQ3YyIsInVzZXJfaWQiOiJmY2E2YjNiNC0yNjQ1LTQ4NTItOTQ4YS03ZjUxZWZkMWRjODcifQ.7cee-lCqquKTHDl0MXK0i9tFjG0FQp6oFVl8l1e5QeU"
}
```

### To get register customer

#### Request

`POST <BASE_URL>/register/customer/`
<br />
Body: `{
    "username":"customer3",
    "email":"customer3@mail.com",
    "password":"customer3"
}`

#### Response

```json
{
    "id": "0d1739ea-ba36-4d1b-add5-e34045a76be5",
    "email": "customer3@mail.com",
    "username": "customer3",
    "user_type": "customer",
    "date_joined": "2021-06-29T17:24:43.532383Z",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI3NTc5NDgzLCJqdGkiOiI1MTBhMzRlNjIwNTc0ZTg5YTZkYmIzOWFkYjY2MjliNCIsInVzZXJfaWQiOiIwZDE3MzllYS1iYTM2LTRkMWItYWRkNS1lMzQwNDVhNzZiZTUifQ.OwrAsVp9CuMzGOG0GMNejlYI6I-WEj5FQkjGSuhGEF4"
}
```

### To get list of user

#### Request

`GET <BASE_URL>/list/`
<br />
Header: `{ 'Authorization':'<TOKEN>' }`

#### Response

Response will be different for different user base on token.
```json
[
    {
        "id": "2f837973-6f08-4ff0-8d18-12f791d30504",
        "email": "customer2@mail.com",
        "username": "customer2",
        "first_name": "customer2",
        "last_name": "customer last",
        "user_type": "customer",
        "date_joined": "2021-06-27T15:26:04.635540Z"
    },
    {
        "id": "f3f5bdac-6bad-496a-adea-b750c821c20d",
        "email": "user5@mail.com",
        "username": "user5",
        "first_name": null,
        "last_name": null,
        "user_type": "agent",
        "date_joined": "2021-06-27T13:58:26.966191Z"
    }
]
```

### To get user

#### Request

`GET <BASE_URL>/<uuid:id>/`
<br />
Header: `{ 'Authorization':'<TOKEN>' }`

#### Response

```json
{
    "id": "2f837973-6f08-4ff0-8d18-12f791d30504",
    "email": "customer2@mail.com",
    "username": "customer2",
    "first_name": "customer2",
    "last_name": "customer last",
    "user_type": "customer",
    "date_joined": "2021-06-27T15:26:04.635540Z"
}
```

### To edit user

#### Request

`PUT <BASE_URL>/<uuid:id>/`
<br />
Body: `
{
    "username":"customer2",
    "email":"customer2@mail.com",
    "password":"customer2",
    "first_name":"customer2 update",
    "last_name":"customer last"
}
`
<br />
Header: `{ 'Authorization':'<TOKEN>' }`

#### Response

```json
{
    "id": "2f837973-6f08-4ff0-8d18-12f791d30504",
    "email": "customer2@mail.com",
    "username": "customer2",
    "first_name": "customer2 update",
    "last_name": "customer last",
    "user_type": "customer",
    "date_joined": "2021-06-27T15:26:04.635540Z"
}
```

#### **BASE_URL**: /api/loan

### To create loan

#### Request

`POST <BASE_URL>/create/`
<br />
Header: `{ 'Authorization':'<TOKEN>' }`
<br />
Body: `{
    'amount': 100000,
    'interest_rate': 10,
    'start_date':'2021/10/12',
    'customer': 'customer2',
    duration: 25
}`

#### Response
Only agent type user is allowed

```json
{
    "id": 23,
    "amount": 10000,
    "interest_rate": 10.0,
    "start_date": "2021-10-12T00:00:00Z",
    "duration": 25,
    "status": "new",
    "emi": "90.87",
    "agent": "user3",
    "customer": "customer2"
}
```

### To get list of loan

#### Request

`POST <BASE_URL>/list/?status=<new|approved|rejected>&created_at='yyyy/mm/dd'&updated_at='yyyy/mm/dd'`
<br />
Header: `{ 'Authorization':'<TOKEN>' }`

#### Response
Response result different for different user.

```json
[
    {
        "id": 17,
        "amount": 10000,
        "interest_rate": 10.0,
        "start_date": "2022-10-12T00:00:00Z",
        "duration": 9,
        "status": "new",
        "emi": "140.79",
        "agent": "user3",
        "customer": "customer2"
    },
    {
        "id": 18,
        "amount": 1200,
        "interest_rate": 12.0,
        "start_date": "2021-06-30T05:50:50Z",
        "duration": 6,
        "status": "new",
        "emi": "23.46",
        "agent": "user3",
        "customer": "customer2"
    },
]
```

### To edit loan

#### Request

`POST <BASE_URL>/edit/<int:id>`
<br />
Header: `{ 'Authorization':'<TOKEN>' }`
<br />
Body: `{
    "amount": 10000,
    "interest_rate": 10.6,
    "start_date": "2022/10/12",
    "duration": 19,
    "agent": "user3",
    "customer": "customer1"
}`

#### Response
Only agent type use can edit

```json
{
    "id": 20,
    "amount": 10000,
    "interest_rate": 10.6,
    "start_date": "2022-10-12T00:00:00Z",
    "duration": 19,
    "status": "new",
    "emi": "102.08",
    "agent": "user3",
    "customer": "customer1"
}
```

### To approved loan

#### Request

`POST <BASE_URL>/<int:id>/approved/`
<br />
Header: `{ 'Authorization':'<TOKEN>' }`

#### Response
Only admin allowed

```json
{
    "success": "Loan is approved."
}
```

### To rejected loan

#### Request

`POST <BASE_URL>/<int:id>/rejected/`
<br />
Header: `{ 'Authorization':'<TOKEN>' }`

#### Response
Only admin allowed

```json
{
    "success": "Loan is rejected."
}
```

## Postman

Use Postman for testing api. Import [lms.postman_collection.json](./lms.postman_collection.json) file on postman to use. As default parameter are set.
Before making any request on postman. First register user of agent and customer type. Then get tokens for admin, agent and customer type uses from login endpoint and paste to environment variable accordingly.

### Status (Incomplete)

React For Front End will be added shortly.
