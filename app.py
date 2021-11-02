from flask import Flask, request
import pymysql
 

app = Flask(__name__)

app.config['MYSQL_USER'] = 'sql5448320'
app.config['MYSQL_PASSWORD'] = '1HYmpBYzky'
app.config['MYSQL_HOST'] = 'sql5.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql5448320'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = pymysql.connection.cursor()
        pymysql.connection.commit()
        cursor.close()
        return f"Done!!"
 
app.run(host='sql5.freemysqlhosting.net', port=3306)