# The CI/CD pipeline
[![CI Pipeline](https://github.com/linux-training-group-1/asset-registry/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/linux-training-group-1/asset-registry/actions/workflows/ci.yml)
[![CodeQL](https://github.com/linux-training-group-1/asset-registry/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/linux-training-group-1/asset-registry/actions/workflows/codeql-analysis.yml)

![cicd-full](https://user-images.githubusercontent.com/32504465/151090833-ecf8d08c-fb2e-4598-996c-1f10ffb76765.png)




# Asset Registry Application
## High level architecture
![finalarch](https://user-images.githubusercontent.com/32504465/151090728-cd94b352-93b2-4798-9dca-a8eb3e222917.png)


## Developer Guide
Create a virtual environment and activate it.
Install the dependencies:<br>
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
Used for check the code while developing <br>
Install requirements:<br>
```pip install -r requirements.txt```<br>
Start the application:<br>
This will reload the app on file changes.<br>
```python3 run_locally.py```<br>


## Run the complete setup locally
Start the setup<br>
```docker-compose up```<br>
<br>
We need to create the database tables and insert dummy data (Only needed the first time runing this setup)<br>
Login to mysql <br>
```mysql -h localhost -P 3306 --protocol=tcp -u root -p```<br>
Create mysql database and tables <br>
```source scripts/table.sql```<br>
Add dummy data<br>
```source scripts/inserts.sql```<br>
If you want to start the mysql container only, use:<br>
``` docker-compose up mysql```


## Build the docker image 
To check if the docker image is working after changing the Dockerfile<br>
Build the docker image<br>
```docker build -t asset-app .```<br>
Start the docker image<br>
```docker run --env-file=.env -itp 5000:5000 asset-app```<br>
