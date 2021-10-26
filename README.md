# asset-registry
## Run locally
Install requirements:<br>
```pip install -r requirements.txt```<br>
Run:<br>
```gunicorn --bind 0.0.0.0:5000 app:app```<br>
## Run on Docker
Build the docker image<br>
```docker build -t asset-app .```<br>
Start the docker image<br>
```docker run -itp 5000:5000 asset-app```<br>
