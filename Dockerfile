FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update
RUN apt-get upgrade
RUN apt-get -y install iproute2
RUN apt-get -y install htop

CMD ["sleep","infinity"]

