FROM python:3.8-alpine3.14

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt
RUN pytest
# run unit tests

EXPOSE 5000
CMD ["gunicorn", "app:app","-b",":5000"]