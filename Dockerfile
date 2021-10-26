FROM python:3.8

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt
#RUN apt update
#RUN apt install gunicorn

#ENTRYPOINT ["python"]
EXPOSE 5000
CMD ["gunicorn", "app:app","-b","0.0.0.0:5000"]