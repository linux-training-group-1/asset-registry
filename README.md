# Asset Registry
[![CI Pipeline](https://github.com/linux-training-group-1/asset-registry/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/linux-training-group-1/asset-registry/actions/workflows/ci.yml)
[![CodeQL](https://github.com/linux-training-group-1/asset-registry/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/linux-training-group-1/asset-registry/actions/workflows/codeql-analysis.yml)
## Test the app
Install dependencies:<br>
```pip install -r requirements.txt -r requirements-dev.txt```<br>
Run tests:<br>
```pytest --verbose --failed-first```<br>

## Run locally
Install requirements:<br>
```pip install -r requirements.txt```<br>
Start the application:<br>
```python3 app.py```<br>

## Run the app on Docker
Build the docker image<br>
```docker build -t asset-app .```<br>
Start the docker image<br>
```docker run -itp 5000:5000 asset-app```<br>

## Run the app + redis + mysql 
Start the setup<br>
```docker-compose up```<br>
<br>
(First time only)<br>
Login to mysql <br>
```mysql -h localhost -P 3306 --protocol=tcp -u root -p```<br>
Create mysql database and tables <br>
```source table.sql```<br>
