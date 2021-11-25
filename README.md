# Asset Registry
[![CI Pipeline](https://github.com/linux-training-group-1/asset-registry/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/linux-training-group-1/asset-registry/actions/workflows/ci.yml)
[![CodeQL](https://github.com/linux-training-group-1/asset-registry/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/linux-training-group-1/asset-registry/actions/workflows/codeql-analysis.yml)

Install dependencies:<br>
```pip install -r requirements.txt -r requirements-dev.txt```<br>
Create a `.env` file on the project root. Add the following:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DB=asset_app
MYSQL_PORT=3306
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
SECRET_KEY=bff4eb94deb028b293786461
```
Run tests:<br>
```pytest --verbose --failed-first```<br>
Install MySQL and Redis if running locally<br>

## Run locally
Install requirements:<br>
```pip install -r requirements.txt```<br>
Start the application:<br>
```python3 run_locally.py```<br>

## Run the app on Docker
Build the docker image<br>
```docker build -t asset-app .```<br>
Start the docker image<br>
```docker run --env-file=.env -itp 5000:5000 asset-app```<br>

## Run the app + redis + mysql 
Start the setup<br>
```docker-compose up```<br>
<br>
(First time only)<br>
Login to mysql <br>
```mysql -h localhost -P 3306 --protocol=tcp -u root -p```<br>
Create mysql database and tables <br>
```source scripts/table.sql```<br>
Add dummy data<br>
```source scripts/inserts.sql```<br>


<br>
A valid jwt token: <br>
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhc3NldC1hcHAiLCJzdWIiOiJib2IiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0IiwiaWF0IjoxNjM3MTY1MDA2LCJuYmYiOjE2MzcxNjUwMDYsImV4cCI6MTYzOTc1NzAwNiwianRpIjoiNDFhMjk4MjctNjQ5ZS00NGQzLThiOGUtMGI3MzgwOWE2ZjJhIn0.tIzBl4rbqLFPtjLgW60ynVvkTBfSqVVTOeeoji7FH_M
```
