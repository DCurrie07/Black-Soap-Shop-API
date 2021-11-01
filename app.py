from logging import debug
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'b80e6664a2dc60'
app.config['MYSQL_DATABASE_PASSWORD'] = '79eb48e5'
app.config['MYSQL_DATABASE_DB'] = 'heroku_f1cb21ef63afad5'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-04.cleardb.com'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE user (id INTEGER, name VARCHAR(20))''')

    #cur.execute('''INSERT INTO example VALUES (1, 'Anthony')''')
    #cur.execute('''INSERT INTO example VALUES (2, 'Billy')''')
    #mysql.connection.commit()

    cur.execute('''SELECT * FROM user''')
    results = cur.fetchall()
    print(results)
    return (results)


if __name__ == "__main__":
    app.run(debug=True)