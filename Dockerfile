FROM python:3.10

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y postgresql-client

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000