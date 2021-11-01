from flask import Flask
import pymysql

app = Flask(__name__)

@app.route('/admin')
def mysqlconnect():
	# To connect MySQL database
	conn = pymysql.connect(
		host='us-cdbr-east-04.cleardb.com',
		user='b80e6664a2dc60',
		password = "79eb48e5",
		db='heroku_f1cb21ef63afad5',
		)
	
	cur = conn.cursor()
	
	# Select query
	cur.execute("select * from admin")
	output = cur.fetchall()
	
	for i in output:
		print(i)
	
	# To close the connection
	conn.close()

# Driver Code
if __name__ == "__main__" :
	mysqlconnect()
