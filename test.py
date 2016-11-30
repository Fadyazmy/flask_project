from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

@app.route("/")
def hello():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    query = ("SELECT * from Customer")
    cursor.execute(query)
    users=cursor.fetchall()
    cnx.close()
    return render_template('users.html',users=users)

@app.route('/entername')
def helloName(name=None):
    return render_template('form.html', name=name)

@app.route('/submit', methods=["POST"])
def submit():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = (
        "INSERT INTO Customer (firstname, lastname, EmailAddress, Sex) "
        "VALUES (%s, %s, %s, %s)"
    )
    data = (request.form['firstname'], request.form['lastname'], request.form['email'], request.form['sex'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return render_template('index.html', firstname=request.form['firstname'], lastname=request.form['lastname'], email=request.form['email'], sex=request.form['sex'])

@app.route('/sqlInjection')
def sqlInjection(name=None):
    return render_template('form2.html')

@app.route('/submitSqlInjection', methods=["POST"])
def sqlInjectionResult():
    cnx = mysql.connector.connect(user='root', database='mydb')
    cursor = cnx.cursor()

    firstName = request.form['firstname']
    query = ("SELECT * from Customer where firstname = '" + firstName + "'")
    cursor.execute(query)
    print("Attempting: " + query)
    users=cursor.fetchall()

    cnx.commit()
    cnx.close()
    return str(users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
