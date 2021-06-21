# import main Flask class and request object
from flask import Flask, render_template, request
import sqlite3 as sql
from flask import jsonify

# https://pythonbasics.org/flask-sqlite/

# create the Flask app
app = Flask(__name__)


# show home page
@app.route('/')
def home():
   return render_template('home.html')

# show form page to add items into database
@app.route('/enternew')
def new_student():
   return render_template('student.html')

# after add items, auotmatically return the results
@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html", msg = msg)
         con.close()

# show all items in database
@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)

# # GET requests will be blocked
# @app.route('/json-example', methods=['POST'])
# def json_example():
#     request_data = request.get_json()

#     print(request_data)
#     return jsonify(request_data)

# read all records from database and passed them to the list.html template.




if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
