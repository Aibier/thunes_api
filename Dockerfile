FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./entrypoint.sh /code/entrypoint.sh
COPY . /code/
ENTRYPOINT ["/code/entrypoint.sh"]

