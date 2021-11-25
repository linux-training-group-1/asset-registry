FROM python:3.8-slim

ARG PORT=5000

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt

RUN groupadd -g 61000 assetuser && useradd -g 61000 -l -M -s /bin/false -u 61000 assetuser
USER assetuser

EXPOSE $PORT
ENTRYPOINT ["gunicorn"]
CMD ["asset_app:app","-b",":5000"]

HEALTHCHECK --interval=5m --timeout=3s CMD wget --no-verbose  --spider http://localhost:5000/api/health || exit 1