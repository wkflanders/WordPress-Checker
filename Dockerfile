# Dockerfile, Image, Container
FROM python:3.10.5

WORKDIR /app

ADD . /app

RUN pip install requests

EXPOSE 80

CMD [ "python", "./wordpress_checker.py" ]