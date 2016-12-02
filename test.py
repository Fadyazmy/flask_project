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


# cnx = mysql.connector.connect(user='root', database='mydb')
# cursor = cnx.cursor()
# query = ("SELECT * from Customer where firstname = '" + firstName + "'")
# cursor.execute(query)
# print("Attempting: " + query)
# users = cursor.fetchall()
#
# cnx.commit()
# cnx.close()

@app.route('/back-end/<type>')
def movies(type=None):
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    query=None
    if type == "movies":
        query = ("SELECT * FROM Movie ORDER BY MovieName ASC ")
    elif type == "genres":
        query = ("SELECT * FROM Genre ORDER BY Genre ASC ") #TODO: FIND INERSECT TO RETURN MOVIE NAME
    elif type == "rooms":
        query = ("SELECT * FROM TheatreRoom") #TODO: FIND INERSECT TO RETURN MOVIE NAME

    cursor.execute(query)
    list = cursor.fetchall()
    return render_template('form.html', formType=type, list=list )



@app.route('/submit/<actionType>/<subType>', methods=["POST"])
def submit(subType=None, actionType=None):
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = None
    data = None
    test = None
    #############MOVIES
    if subType == "movies":
        # Filer request by type of modification
        if actionType == "add":
            insert_stmt = (
                "INSERT INTO Movie (MovieName, MovieYear) "
                "VALUES (%s, %s)"
            )
            data = (request.form['movieName'], request.form['movieYear'])
            test = request.form['movieName']
            print "INSERTING MOVIE" + test
        elif actionType == "delete":
            insert_stmt = (
                "DELETE FROM Movie WHERE MovieName =%s AND MovieYear=%s "
            )
            data = (request.form['movieName'], request.form['movieYear'])
            test = request.form['movieName']
        elif actionType == "update":
            insert_stmt = (""" UPDATE Movie
                        SET MovieName = %s, MovieYear = %s
                        WHERE idMovie = %s """)
            data = (request.form['movieName'],request.form['movieYear'], request.form['idMovie'])
            test = request.form['movieName']




    #############GENRES
    elif subType == "genre":
        if actionType == "add":
            insert_stmt = (
                    "INSERT INTO GENRE (Genre, Movie_idMovie) "
                    "VALUES (%s, %s)"
                )
            data = (request.form['Genre'], request.form['Movie_idMovie'])
            test = request.form['Genre']
        elif actionType =="del":
            insert_stmt = (
                "DELETE FROM Genre WHERE Genre =%s AND Movie_idMovie=%s "
            )
            data = (request.form['Genre'], request.form['Movie_idMovie'])
            test = request.form['Genre']




    #############ROOMS
    elif subType == "rooms":
        if actionType == "add":
            insert_stmt = (
                "INSERT INTO TheatreRoom (RoomNumber, Capacity) "
                "VALUES (%s, %s)"
            )
            data = (request.form['RoomNumber'], request.form['Capacity'])
            test = request.form['RoomNumber']
        elif actionType == "delete":
            insert_stmt = (
                "DELETE FROM TheatreRoom WHERE RoomNumber =%s"
            )
            data = (request.form['RoomNumber'])
            test = request.form['RoomNumber']



    elif subType == "customer":
        insert_stmt = (
            "INSERT INTO Customer (FirstName, LastName, EmailAddress, Sex) "
            "VALUES (%s, %d)"
        )
        data = (request.form['movieName'], request.form['Movie_idMovie'])
    else:
        subType == "attend"
        insert_stmt = (
            "INSERT INTO Attend (Showing_idShowing, Rating) "
            "VALUES (%s,   %d)"
        )
        data = (request.form['movieName'], request.form['Movie_idMovie'])

    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return render_template('index2.html', formType=subType, test = test, actionType = actionType)




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
