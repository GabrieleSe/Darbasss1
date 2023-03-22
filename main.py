from flask import Flask, render_template, request
import sqlite3
connection=sqlite3.connect(".\\NotesDatabase.db")

variable=0
array=[]
res=[]

app = Flask(__name__,static_url_path='')
variable=0

@app.route("/")
def mano_funkcija():
    return ("Labas")

@app.route("/test")
def test_route():
    if (request.args.get("name")):
        plus_one()
    return render_template('./index.html', var=plus_one())

@app.route("/debug")
def plus_one():
    global variable
    variable = variable +1
    return str(variable)

@app.route("/notes",methods=["GET","POST"])
def notes():
    array_2 = select_from_db()
    if(request.method == "POST"):
        global array 
        global res
        args=request.form.get("note2")
        if(args):
            array.append(args)
            insert_into_db(args)
            res=array[::-1]
            print(res)
            
        return render_template('./notes.html', note=select_from_db())
    else:
        return render_template('./notes.html', note=select_from_db())
    

@app.route("/registracija",methods=["GET","POST"])
def registracija():
    if(request.method == "POST"):
        email=request.form.get("email")
        pasword=request.form.get("psw")
        insert_user_db(email,pasword)
    return render_template("./registracija.html")

def createDB():

    global connection
    cursor=connection.cursor()
    createTableString = """CREATE TABLE IF NOT EXISTS Sheets (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL
    )"""

    createNotesTableString = """CREATE TABLE IF NOT EXISTS Notes (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        SheetId INTEGER NOT NULL,
        Header TEXT
        Text TEXT,
        FOREIGN KEY (SheetId) REFERENCES Sheets(Id)
    )"""
    createVartotojasTableString = """CREATE TABLE IF NOT EXISTS Vartotojas (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Email TEXT NOT NULL,
        Pasword TEXT NOT NULL
    )"""
    
    cursor.execute(createTableString)
    cursor.execute(createNotesTableString)
    cursor.execute(createVartotojasTableString)

def insert_into_db(note):
    connection=sqlite3.connect(".\\NotesDatabase.db")
    queryString="""
        INSERT INTO Sheets (Name) VALUES (?) 
    """
    cur=connection.cursor()
    cur.execute(queryString,(note,))
    connection.commit()

def insert_user_db(Email,Pasword):
    connection=sqlite3.connect(".\\NotesDatabase.db")
    queryString="""
        INSERT INTO Vartotojas (Email, Pasword) VALUES (?,?) 
    """
    cur=connection.cursor()
    cur.execute(queryString,(Email,Pasword))
    connection.commit()

def select_from_db():
    connection=sqlite3.connect(".\\NotesDatabase.db")
    queryString="""
        SELECT name FROM Sheets
    """
    cur=connection.cursor()
    array = cur.execute(queryString).fetchall()
    return array 

if __name__ =="__main__":
    createDB()
    app.run(debug="true")
