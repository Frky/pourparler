FROM python:2.7

RUN apt-get update
RUN apt-get -y install rubygems ruby-full
RUN gem install --no-rdoc --no-ri sass -v 3.4.22
RUN gem install --no-rdoc --no-ri compass

RUN pip install uwsgi

RUN mkdir -p /app/eloquence
COPY requirements.txt /app/eloquence
WORKDIR /app

RUN pip install -r eloquence/requirements.txt

COPY ./ /app/
WORKDIR /app
RUN ls
RUN compass compile

WORKDIR /app

RUN ./manage.py collectstatic --noinput -c

CMD uwsgi \
        --http :8000 \
        --module eloquence.wsgi \
        --socket eloquence.sock \
        --chmod-socket=776
