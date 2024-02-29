FROM python:3.12
WORKDIR /email-backend
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./.env .env
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]
