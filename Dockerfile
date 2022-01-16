FROM python:3.10.1 as build-image

RUN apt-get update && apt-get upgrade -y
RUN apt-get install --reinstall build-essential --no-install-recommends -y
#RUN apt-get install -y --no-install-recommends gcc

## virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

## add and install requirements
RUN pip install --upgrade pip && pip install pip-tools
COPY requirements.txt .
RUN pip install -r requirements.txt




FROM python:3.10.1-slim AS runtime-image

RUN apt-get update && apt-get upgrade -y

## copy Python dependencies from build image
COPY --from=build-image /opt/venv /opt/venv

## set working directory
WORKDIR /usr/src/app

## add user
RUN addgroup --system user && adduser --system --no-create-home --group user
RUN chown -R user:user /usr/src/app && chmod -R 755 /usr/src/app

USER user

## add app
COPY . /usr/src/app

## set environment variables
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 5000
ENTRYPOINT ["gunicorn"]
CMD ["asset_app:app","-b",":5000","--workers","4","--log-level","debug","--worker-class","gevent","--preload"]

HEALTHCHECK --interval=5m --timeout=3s CMD wget --no-verbose  --spider http://localhost:5000/health || exit 1
