# pull official base image
FROM alpine:3.7
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apk update \
    && apk add gcc bash python3-dev python3 py3-pip libxml2-dev musl-dev \
    && apk add postgresql postgresql-dev \
    && pip3 install psycopg2-binary \
    && pip3 install virtualenv 

RUN virtualenv --python=python3 venv
	
RUN source venv/bin/activate \
	&& pip install --upgrade pip


# install dependencies
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r /usr/src/app/requirements.txt

# copy entrypoint.sh
COPY entrypoint.sh /usr/src/app/entrypoint.sh
COPY setup_env.py /usr/src/app/setup_env.py
# copy project
COPY . /usr/src/app/
# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
