#!/bin/sh
# Runs on every start of the Netbox Docker container

# Stop when an error occures
set -e

# Give time for the database server to initialize
echo "⏳ Waiting 10 seconds for the database server to initialize"
sleep 10s

cd "$NETBOX_HOME"
cp /app/development/sap_netbox_dev.svg /opt/netbox/netbox/project-static/img/netbox_logo.svg
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
