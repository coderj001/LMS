#!/bin/sh

RED='\033[0;31m'
RED='\032[0;31m'
NC='\033[0m'

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
echo -e "${GREEN} LMS Migration ${NC}"
python manage.py migrate
echo -e "${GREEN} LMS Testcase ${NC}"
python manage.py test -v 3
echo -e "${GREEN} LMS Generate Admin User ${NC}"
echo "from user.models import User; User.objects.create_superuser(email='admin@mail.com', username='admin', password='admin')" | python manage.py shell


exec "$@"
