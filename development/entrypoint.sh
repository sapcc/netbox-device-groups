#!/bin/sh
# Runs on every start of the Netbox Docker container

# Stop when an error occures
set -e

# Give time for the database server to initialize
echo "⏳ Waiting 3 seconds for the database server to initialize"
sleep 3

#If there is database backup file to restore, restore the database.
BACKUP_FILE="/app/development/backup/netbox.bkp"

if [ -e $BACKUP_FILE ]; then
    echo "💡 We have a database backup file $BACKUP_FILE to restore"
    psql -t -U $NETBOX_DB_USER -h $NETBOX_DB_HOST -d $NETBOX_DB_NAME -f development/backup/test_db.sql | sed -e 's/^[[:space:]]*//' | sed 's/\r$//' > /app/development/backup/tables.out
    read -r has_data < /app/development/backup/tables.out
    if [ "$has_data" = "0" ] ; then
        echo "⏳ The Netbox database needs to be restored, restoring."
        pg_restore -U $NETBOX_DB_USER -h $NETBOX_DB_HOST -d $NETBOX_DB_NAME $BACKUP_FILE
    else
        echo "💡 The Netbox database has already been restored, continuing."
    fi
fi

cd "$NETBOX_HOME"
cp /app/development/netbox_dev.svg /opt/netbox/netbox/project-static/img/netbox_logo.svg
# Prepare the web static content
echo "⏳ Running initial systems check..."
python3 manage.py migrate
python3 manage.py collectstatic --noinput

# Nõw for some jiggery pokery in the background to setup a superuser for development.
cat <<EOP | python3 manage.py shell
from django.contrib.auth.models import User
from users.models import Token
u = User.objects.filter(username='${NETBOX_SUPERUSER_NAME}')
if not u:
    u = User.objects.create_superuser('${NETBOX_SUPERUSER_NAME}', '${NETBOX_SUPERUSER_EMAIL}', '${NETBOX_SUPERUSER_PASSWORD}')
    Token.objects.create(user=u, key='${NETBOX_SUPERUSER_API_TOKEN}')
else:
    u = u[0]
    if u.email != '${NETBOX_SUPERUSER_EMAIL}':
        u.email = '${NETBOX_SUPERUSER_EMAIL}'
    if not u.check_password('${NETBOX_SUPERUSER_PASSWORD}'):
        u.set_password('${NETBOX_SUPERUSER_PASSWORD}')
    u.save()
    t = Token.objects.filter(user=u)
    if t:
        t = t[0]
        if t.key != '${NETBOX_SUPERUSER_API_TOKEN}':
            t.key = '${NETBOX_SUPERUSER_API_TOKEN}'
            t.save()

exit()
EOP

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "💡 Superuser Username: ${NETBOX_SUPERUSER_NAME}, E-Mail: ${NETBOX_SUPERUSER_EMAIL}, Password ${NETBOX_SUPERUSER_PASSWORD}"

# Launch netbox
exec python3 manage.py runserver 0.0.0.0:8080 --insecure
