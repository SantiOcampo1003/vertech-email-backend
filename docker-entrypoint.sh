#!/bin/sh

flask db init

flask db migrate

flask db upgrade

exec gunicorn --bind 0.0.0.0:5000 "app.app:create_app()"
