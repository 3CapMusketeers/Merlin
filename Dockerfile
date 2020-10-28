# base image
FROM python:3.8.1-slim

# install netcat
RUN apt-get update && \
    apt-get -y install netcat libsndfile1-dev && \
    apt-get clean

RUN mkdir /data
# set working directory
WORKDIR /usr/src/app

ENV NGINX_WORKER_CONNECTIONS 2048
ENV NGINX_WORKER_OPEN_FILES 2048

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# add appi
COPY . /usr/src/app

EXPOSE 5005

RUN chmod +x /usr/src/app/entrypoint.sh

# run server
CMD ["/usr/src/app/entrypoint.sh"]