FROM python:3.8-alpine3.14

ARG PORT=5000

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

RUN addgroup -S assetuser && adduser -S -G assetuser assetuser
USER assetuser

EXPOSE $PORT
CMD ["gunicorn", "app:app","-b",":5000"]

HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost:$PORT/ || exit 1