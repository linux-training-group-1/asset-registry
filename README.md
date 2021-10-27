# asset-registry
## Run locally
Install requirements:<br>
```pip install -r requirements.txt```<br>
Run tests:<br>
```pytest```<br>
Start the application:<br>
```gunicorn --bind 0.0.0.0:5000 app:app```<br>
## Run on the app on Docker
Build the docker image<br>
```docker build -t asset-app .```<br>
Start the docker image<br>
```docker run -itp 5000:5000 asset-app```<br>
## Run the app + redis + mysql
```docker-compose up```<br>