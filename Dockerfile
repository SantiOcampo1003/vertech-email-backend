FROM python:3.12-alpine
WORKDIR /email-backend
RUN apk add --no-cache gcc musl-dev linux-headers bash
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./.env .env
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]
