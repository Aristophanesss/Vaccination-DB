# Reference:
# Citation for the basic framework of backend:
# Date: 17/05/2022
# Modified from: flask-starter-app
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app


from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


# Configuration
app = Flask(__name__)

# Database Connection
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_xueche"
app.config["MYSQL_PASSWORD"] = "XXXX"
app.config["MYSQL_DB"] = "cs340_xueche"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


# Routes 
@app.route('/')
def root():
    return render_template("index.j2")

# Index
@app.route('/index')
def index():
    return render_template("index.j2")

# Institutions
@app.route('/institutions', methods=["POST", "GET"])
def institutions():
    if request.method == "GET":
        query = "SELECT institutionID, institutionName, (CASE WHEN publicInstituion = 1 THEN 'Yes' ELSE 'No' END) AS Public FROM Institutions WHERE institutionID>0"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("institutions.j2", data=data)

    if request.method == "POST":
        if request.form.get("Add_institutions"):
            Institution = request.form["Institution"]
            Public = request.form["Public"]
            
            query = "INSERT INTO Institutions (institutionName, publicInstituion) VALUES (%s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (Institution, Public))
            mysql.connection.commit()
            return redirect("/institutions")

# Records
@app.route('/records', methods=["POST", "GET"])
def records():
    if request.method == "GET":
        query = "SELECT Records.recordID, Residents.residentName, Vaccines.targetDisease, Vaccines.vaccineManufacturer, Institutions.institutionName, Records.inoculationDate, Records.doseCount FROM Records JOIN Residents ON Records.residentID = Residents.residentID JOIN Vaccines ON Records.vaccineID = Vaccines.vaccineID JOIN Institutions on Records.institutionID = Institutions.institutionID ORDER BY Records.recordID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT residentName FROM Residents ORDER BY residentName"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        resident = cur.fetchall()

        query3 = "SELECT targetDisease FROM Vaccines GROUP BY targetDisease ORDER BY targetDisease"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        target = cur.fetchall()

        query4 = "SELECT vaccineManufacturer FROM Vaccines GROUP BY vaccineManufacturer ORDER BY vaccineManufacturer"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        manufacturer = cur.fetchall()

        query5 = "SELECT institutionName from Institutions GROUP BY institutionName ORDER BY institutionName"
        cur = mysql.connection.cursor()
        cur.execute(query5)
        institutionName = cur.fetchall()

        query6 = "SELECT targetDisease, vaccineManufacturer FROM Vaccines ORDER BY targetDisease"
        cur = mysql.connection.cursor()
        cur.execute(query6)
        vacc = cur.fetchall()
        return render_template("records.j2", data=data, resident=resident, target=target, manufacturer=manufacturer, institutionName=institutionName, vacc=vacc)

    if request.method == "POST":
        if request.form.get("Add_records"):
            Resident = request.form["Resident"]
            Vaccine = request.form["Vaccine"]
            Manufacturer = request.form["Manufacturer"]
            Institution = request.form["Institution"]
            Date = request.form["Date"]
            Dose = request.form["Dose"]
            
            query = "INSERT INTO Records (residentID, vaccineID, institutionID, inoculationDate, doseCount) VALUES ((SELECT residentID FROM Residents WHERE residentName = %s),(SELECT vaccineID FROM Vaccines WHERE targetDisease = %s and vaccineManufacturer = %s), (SELECT institutionID FROM Institutions WHERE institutionName = %s), %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (Resident, Vaccine, Manufacturer, Institution, Date, Dose))
            mysql.connection.commit()
            return redirect("/records")


# Edit Records
@app.route('/edit_records/<int:recordID>', methods=["POST", "GET"])
def edit_records(recordID, ):
    if request.method == "GET":
        query = "SELECT Records.recordID, Residents.residentName, Vaccines.targetDisease, Vaccines.vaccineManufacturer, Institutions.institutionName, Records.inoculationDate, Records.doseCount FROM Records JOIN Residents ON Records.residentID = Residents.residentID JOIN Vaccines ON Records.vaccineID = Vaccines.vaccineID JOIN Institutions on Records.institutionID = Institutions.institutionID WHERE Records.recordID='%s'"
        cur = mysql.connection.cursor()
        cur.execute(query, (recordID, ))
        data1 = cur.fetchall()

        query2 = "SELECT institutionName FROM Institutions ORDER BY institutionName"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        data2 = cur.fetchall()

        query3 = "SELECT targetDisease, vaccineManufacturer FROM Vaccines ORDER BY targetDisease"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        data3 = cur.fetchall()

        query4 = "SELECT targetDisease FROM Vaccines GROUP BY targetDisease ORDER BY targetDisease"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        data4 = cur.fetchall()

        query5 = "SELECT vaccineManufacturer FROM Vaccines GROUP BY vaccineManufacturer ORDER BY vaccineManufacturer"
        cur = mysql.connection.cursor()
        cur.execute(query5)
        data5 = cur.fetchall()

        query6 = "SELECT residentName FROM Residents ORDER BY residentName"
        cur = mysql.connection.cursor()
        cur.execute(query6)
        data6 = cur.fetchall()
        return render_template("edit_records.j2", data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6)
    
    if request.method == "POST":
        if request.form.get("Edit_record"):
            Resident = request.form["Resident"]
            Vaccine = request.form["Vaccine"]
            Manufacturer = request.form["Manufacturer"]
            Institution = request.form["Institution"]
            Date = request.form["Date"]
            Dose = request.form["Dose"]
            
            query = "INSERT INTO Records (residentID, vaccineID, institutionID, inoculationDate, doseCount) VALUES ((SELECT residentID FROM Residents WHERE residentName = %s),(SELECT vaccineID FROM Vaccines WHERE targetDisease = %s and vaccineManufacturer = %s), (SELECT institutionID FROM Institutions WHERE institutionName = %s), %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (Resident, Vaccine, Manufacturer, Institution, Date, Dose))
            mysql.connection.commit()

            query = "DELETE FROM Records WHERE recordID = '%s'"
            cur = mysql.connection.cursor()
            cur.execute(query, (recordID, ))
            mysql.connection.commit()
            return redirect("/records")

# Residents
@app.route('/residents', methods=["POST", "GET"])
def residents():
    if request.method == "GET":
        query = "SELECT * FROM Residents"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("residents.j2", data=data)

    if request.method == "POST":
        if request.form.get("Add_resident"):
            Name = request.form["Name"]
            Date = request.form["Date"]
            Allergy = request.form["Allergy"]
            Disease = request.form["Disease"]

            if Allergy == "":
                Allergy = "None"
            if Disease == "":
                Disease = "None"
            
            query = "INSERT INTO Residents (residentName, birthDate, allergyHistory, diseaseHistory) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (Name, Date, Allergy, Disease))
            mysql.connection.commit()
            return redirect("/residents")

# Vaccines
@app.route('/vaccines', methods=["POST", "GET"])
def vaccines():
    if request.method == "GET":
        query = "SELECT * FROM Vaccines"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("vaccines.j2", data=data)

    if request.method == "POST":
        if request.form.get("Add_vaccine"):
            Name = request.form["Name"]
            Type = request.form["Type"]
            Manufacturer = request.form["Manufacturer"]
            
            query = "INSERT INTO Vaccines (targetDisease, vaccineType, vaccineManufacturer) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (Name, Type, Manufacturer))
            mysql.connection.commit()
            return redirect("/vaccines")

# Inventories
@app.route("/inventories", methods=["POST", "GET"])
def inventories():
    if request.method == "GET":
        query = "SELECT Inventories.institutionID, Institutions.institutionName, Inventories.vaccineID, Vaccines.targetDisease, Vaccines.vaccineManufacturer from Inventories JOIN Institutions on Inventories.institutionID = Institutions.institutionID JOIN Vaccines on Inventories.vaccineID = Vaccines.vaccineID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query1 = "SELECT institutionName from Institutions GROUP BY institutionName ORDER BY institutionName"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        institutionName = cur.fetchall()

        query2 = "SELECT targetDisease, vaccineManufacturer FROM Vaccines ORDER BY targetDisease"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        vacc = cur.fetchall()

        query3 = "SELECT targetDisease FROM Vaccines GROUP BY targetDisease ORDER BY targetDisease"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        target = cur.fetchall()

        query4 = "SELECT vaccineManufacturer FROM Vaccines GROUP BY vaccineManufacturer ORDER BY vaccineManufacturer"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        manufacturer = cur.fetchall()
        return render_template("inventories.j2", data=data, institutionName=institutionName, vacc=vacc, target=target, manufacturer=manufacturer)

    if request.method == "POST":
        if request.form.get("Add_inventory"):
            Institution = request.form["Institution"]
            Vaccine = request.form["Vaccine"]
            Manufacturer = request.form["Manufacturer"]

            query = "INSERT INTO Inventories (institutionID, vaccineID) VALUES ((SELECT institutionID FROM Institutions WHERE institutionName = %s),(SELECT vaccineID FROM Vaccines WHERE targetDisease = %s and vaccineManufacturer = %s))"
            cur = mysql.connection.cursor()
            cur.execute(query, (Institution, Vaccine, Manufacturer))
            mysql.connection.commit()
            return redirect("/inventories")

@app.route('/delete_inventories/<int:institutionID>/<int:vaccineID>')
def delete_inventories(institutionID,vaccineID):
    """Delete function for inventories"""
    query = "DELETE FROM Inventories WHERE institutionID = '%s' and vaccineID = '%s' LIMIT 1;"
    cur = mysql.connection.cursor()
    cur.execute(query, (institutionID, vaccineID))
    mysql.connection.commit()
    return redirect("/inventories")

# Edit Inventories
@app.route('/edit_inventories/<int:institutionID>/<int:vaccineID>', methods=["POST", "GET"])
def edit_inventories(institutionID,vaccineID):
    if request.method == "GET":
        query = "SELECT Inventories.institutionID, Institutions.institutionName, Inventories.vaccineID, Vaccines.targetDisease, Vaccines.vaccineManufacturer from Inventories JOIN Institutions on Inventories.institutionID = Institutions.institutionID JOIN Vaccines on Inventories.vaccineID = Vaccines.vaccineID WHERE Inventories.institutionID = '%s' and Inventories.vaccineID = '%s'"
        cur = mysql.connection.cursor()
        cur.execute(query, (institutionID, vaccineID))
        data1 = cur.fetchall()

        query2 = "SELECT institutionName FROM Institutions ORDER BY institutionName"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        data2 = cur.fetchall()

        query3 = "SELECT targetDisease, vaccineManufacturer FROM Vaccines ORDER BY targetDisease"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        data3 = cur.fetchall()

        query4 = "SELECT targetDisease FROM Vaccines GROUP BY targetDisease ORDER BY targetDisease"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        data4 = cur.fetchall()

        query5 = "SELECT vaccineManufacturer FROM Vaccines GROUP BY vaccineManufacturer ORDER BY vaccineManufacturer"
        cur = mysql.connection.cursor()
        cur.execute(query5)
        data5 = cur.fetchall()
        return render_template("edit_inventories.j2", data1=data1, data2=data2, data3=data3, data4=data4, data5=data5)


    if request.method == "POST":
        if request.form.get("Edit_inventory"):
            Institution = request.form["Institution"]
            Vaccine = request.form["Vaccine"]
            Manufacturer = request.form["Manufacturer"]
            query = "INSERT INTO Inventories (institutionID, vaccineID) VALUES ((SELECT institutionID FROM Institutions WHERE institutionName = %s),(SELECT vaccineID FROM Vaccines WHERE targetDisease = %s and vaccineManufacturer = %s))"
            cur = mysql.connection.cursor()
            cur.execute(query, (Institution, Vaccine, Manufacturer))
            mysql.connection.commit()

            query = "DELETE FROM Inventories WHERE institutionID = '%s' and vaccineID = '%s' LIMIT 1;"
            cur = mysql.connection.cursor()
            cur.execute(query, (institutionID, vaccineID))
            mysql.connection.commit()
            return redirect("/inventories")


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9466))
    app.run(port=port, debug=True) 
