FROM python:3.8-alpine3.14

RUN addgroup -S assetuser && adduser -S -G assetuser assetuser
USER assetuser

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD ["gunicorn", "app:app","-b",":5000"]