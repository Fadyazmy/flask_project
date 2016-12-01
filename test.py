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


@app.route("/home")
def home():
    return render_template('index2.html')



@app.route('/back-end/<type>')
def movies(type=None):
    return render_template('form.html', formType=type)





@app.route('/submit/<subType>', methods=["POST"])
def submit(subType=None):
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = None
    data = None
    test = None
    if subType == "movie":
        insert_stmt = (
            "INSERT INTO Movie (MovieName, MovieYear) "
            "VALUES (%s, %d)"
        )
        data = (request.form['movieName'], request.form['movieYear'])
        test = request.form['movieName']
    elif subType == "genre":
        insert_stmt = (
            "INSERT INTO GENRE (Genre, Movie_idMovie) "
            "VALUES (%s, %d)"
        )
        data = (request.form['Genre'], request.form['Movie_idMovie'])
        test = request.form['Genre']
    elif subType == "showing":
        insert_stmt = (
            "INSERT INTO Showing (Genre, Movie_idMovie) "
            "VALUES (%s, %d)"
        )
        data = (request.form['movieName'], request.form['Movie_idMovie'])
    elif subType == "customer":
        insert_stmt = (
            "INSERT INTO Customer (Genre, Movie_idMovie) "
            "VALUES (%s, %d)"
        )
        data = (request.form['movieName'], request.form['Movie_idMovie'])
    elif subType == "attend":
        insert_stmt = (
            "INSERT INTO Customer (Genre, Movie_idMovie) "
            "VALUES (%s, %d)"
        )
        data = (request.form['movieName'], request.form['Movie_idMovie'])

    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return render_template('index2.html', formType=subType, test = test)




# @app.route('/submit', methods=["POST"])
# def submit():
#     cnx = mysql.connector.connect(user='root', database='MovieTheatre')
#     cursor = cnx.cursor()
#     insert_stmt = (
#         "INSERT INTO Customer (firstname, lastname, EmailAddress, Sex) "
#         "VALUES (%s, %s, %s, %s)"
#     )
#     data = (request.form['firstname'], request.form['lastname'], request.form['email'], request.form['sex'])
#     cursor.execute(insert_stmt, data)
#     cnx.commit()
#     cnx.close()
#     return render_template('index.html', firstname=request.form['firstname'], lastname=request.form['lastname'], email=request.form['email'], sex=request.form['sex'])

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
