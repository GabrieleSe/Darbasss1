from flask import Flask, render_template, request
import sqlite3
connection=sqlite3.connect("C:\\Users\\1562038\\Desktop\\NotesDatabase.db")

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
    
    if(request.method == "POST"):
        global array 
        global res
        args=request.form.get("note2")
        if(args):
            array.append(args)
            res=array[::-1]
            print(res)
        return render_template('./notes.html', note=res)
    else:
        return render_template('./notes.html', note=res)


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
    cursor.execute(createTableString)
    cursor.execute(createNotesTableString)

def insert_into_db():
    global connection
    queryString="""
        INSERT INTO Sheets (Name) VALUES (?) 
    """
    cur=connection.cursor()
    cur.execute(queryString,('test',))


if __name__ =="__main__":
    createDB()
    insert_into_db()
    app.run(debug="true")
