from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

## MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'jay'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'jay'
# app.config['MYSQL_DATABASE_DB'] = 'BucketList'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)


@app.route('/')
def main():
    return render_template('templates/index.html')



if __name__ == "__main__":
    app.run(port=5002)
