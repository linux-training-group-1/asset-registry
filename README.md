# Asset Registry
[![CI Pipeline](https://github.com/linux-training-group-1/asset-registry/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/linux-training-group-1/asset-registry/actions/workflows/ci.yml)
[![CodeQL](https://github.com/linux-training-group-1/asset-registry/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/linux-training-group-1/asset-registry/actions/workflows/codeql-analysis.yml)

Install dependencies:<br>
```pip install -r requirements.txt -r requirements-dev.txt```<br>
Create a `.env` file on the project root. Add the following:
```
MYSQL_HOST=localhost
MYSQL_USER=asset-app
MYSQL_PASSWORD=password
MYSQL_DATABASE=asset_db
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
Used for while developing <br>
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
Used to test the complete setup<br>
Start the setup<br>
```docker-compose up```<br>
<br>
We need to create the table structure and insert data (First time only)<br>
Login to mysql <br>
```mysql -h localhost -P 3306 --protocol=tcp -u root -p```<br>
Create mysql database and tables <br>
```source scripts/table.sql```<br>
Add dummy data<br>
```source scripts/inserts.sql```<br>
