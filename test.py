from flask import Flask, render_template, request
import mysql.connector
from werkzeug import secure_filename

app = Flask(__name__)

# @app.route("/")
# def hello():
#     cnx = mysql.connector.connect(user='root', database='MovieTheatre')
#     cursor = cnx.cursor()
#     query = ("SELECT * from Customer")
#     cursor.execute(query)
#     users=cursor.fetchall()
#     cnx.close()
#     return render_template('users.html',users=users)


@app.route("/")
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
        query = ("SELECT * FROM TheatreRoom")
    elif type == "showings":
        query = ("SELECT * FROM Showing ORDER BY ShowingDateTime ASC")
    elif type == "customers":
        query = ("SELECT * FROM Customer ORDER BY LastName ASC")
    elif type == "attend":
        query = ("SELECT FirstName, LastName, idShowing, ShowingDateTime, movieName, Attend.Rating FROM Customer, Showing, Movie, Attend WHERE Attend.Customer_idCustomer = Customer.idCustomer AND Attend.Showing_idShowing = Showing.idShowing AND Showing.Movie_idMovie = Movie.idMovie ORDER BY Attend.Rating ASC")

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
        elif actionType == "delete":
            insert_stmt = (
                        "DELETE FROM Movie WHERE idMovie = %s;"
            )
            data = (request.form['idMovie'],)
            test = request.form['idMovie']

        elif actionType == "update":
            insert_stmt = (""" UPDATE Movie
                        SET MovieName = %s, MovieYear = %s
                        WHERE idMovie = %s """)
            data = (request.form['movieName'],request.form['movieYear'], request.form['idMovie'])
            test = request.form['movieName']




    #############GENRES
    elif subType == "genres":
        if actionType == "add":
            insert_stmt = (
                    "INSERT INTO GENRE (Genre, Movie_idMovie) "
                    "VALUES (%s, %s)"
                )
            data = (request.form['Genre'], request.form['Movie_idMovie'])
            test = request.form['Genre']
        elif actionType =="delete":
            insert_stmt = (
                "DELETE FROM Genre WHERE Genre= %s and Movie_idMovie=%s;"
            )
            data = (request.form['Genre'],request.form['Movie_idMovie'])
            test = request.form['Genre']
            print ("BOOOO" + test)





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
                "DELETE FROM TheatreRoom WHERE RoomNumber = %s;"
            )
            data = (request.form['RoomNumber'],)
            test = request.form['RoomNumber']

        elif actionType == "update":
            insert_stmt = (""" UPDATE TheatreRoom
                                    SET Capacity = %s
                                    WHERE RoomNumber = %s """)
            data = (request.form['Capacity'],request.form['RoomNumber'])
            test = request.form['RoomNumber']



    #############SHOWINGS
    elif subType == "showings":
        if actionType == "add":
            insert_stmt = (
                "INSERT INTO Showing (ShowingDateTime, Movie_idMovie, TheatreRoom_RoomNumber, TicketPrice) "
                "VALUES (%s, %s, %s, %s)"
            )
            data = (request.form['ShowingDateTime'], request.form['Movie_idMovie'], request.form['TheatreRoom_RoomNumber'], request.form['TicketPrice'])
            test = request.form['ShowingDateTime']
        elif actionType == "delete":
            insert_stmt = (
                "DELETE FROM Showing WHERE idShowing =%s"
            )
            data = (request.form['idShowing'],)
            test = request.form['idShowing']
        elif actionType == "update":
            insert_stmt = (""" UPDATE Showing
                                    SET TicketPrice = %s
                                    WHERE idShowing = %s """)
            data = (request.form['TicketPrice'],request.form['idShowing'])
            test = request.form['idShowing']




    #############CUSTOMER
    elif subType == "customers":
        if actionType == "add":
            insert_stmt = (
                "INSERT INTO Customer (FirstName, LastName, EmailAddress, Sex) "
                "VALUES (%s, %s, %s, %s)"
            )
            data = (request.form['FirstName'], request.form['LastName'], request.form['EmailAddress'], request.form['Sex'])
            test = request.form['FirstName']
        elif actionType == "delete":
            insert_stmt = (
                "DELETE FROM Customer WHERE idCustomer =%s"
            )
            data = (request.form['idCustomer'],)
            test = request.form['idCustomer']
        elif actionType == "update":
            insert_stmt = (""" UPDATE Customer
                                    SET FirstName =%s, LastName =%s, EmailAddress =%s, Sex =%s
                                    WHERE idCustomer =%s """)
            data = (request.form['FirstName'],request.form['LastName'], request.form['EmailAddress'],request.form['Sex'],request.form['idCustomer'])
            test = request.form['FirstName']

    #############Attend
    elif subType == "attend":
        if actionType == "add":
            insert_stmt = (
                "INSERT INTO Customer (FirstName, LastName, EmailAddress, Sex) "
                "VALUES (%s, %s, %s, %s)"
            )
            data = (request.form['FirstName'], request.form['LastName'], request.form['EmailAddress'], request.form['Sex'])
            test = request.form['FirstName']
        elif actionType == "delete":
            insert_stmt = (
                "DELETE FROM Customer WHERE idCustomer =%s"
            )
            data = (request.form['idCustomer'])
            test = request.form['idCustomer']
        elif actionType == "update":
            insert_stmt = (""" UPDATE Customer
                               SET FirstName =%s, LastName =%s, EmailAddress =%s, Sex =%s
                               WHERE idCustomer =%s """)
            data = (request.form['FirstName'],request.form['LastName'], request.form['EmailAddress'],request.form['Sex'],request.form['idCustomer'])
            test = request.form['FirstName']



    if(insert_stmt !=None):
        cursor.execute(insert_stmt, data)
        print (cursor._executed)
        cnx.commit()
        cnx.close()
    return render_template('index2.html', formType=subType, test = test, actionType = actionType)




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
