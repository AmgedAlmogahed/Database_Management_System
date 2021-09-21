"""
Assignment: 6b Write a Program to perform following operations on Company Database,
1) Create EmployeeDetails Table with fields EmpID, EmpName, EmpDept and EmpSalary

2) Insert 5 records in EmployeeDetails table

3) Display All the records added in the EmployeeDetails table

4) Update EmpSalary field of the record no 4 and display the updated contents

5) Delete Record using EmpID field and display the remaining contents
Div: I
Batch: I1/B1
Roll No: 05
Name: Amged Almogahed
"""
import mysql.connector

smile = "¯\_(ツ)_/¯"

myDatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

"""Creating new database"""


def createDatabase():
    name = input("Enter Database Name: ")
    cursor = myDatabase.cursor()
    cursor.execute("CREATE DATABASE {}".format(name))
    print(name, "database was created successfully")


"""Show all databases"""


def showDatabases():
    cursor = myDatabase.cursor()
    cursor.execute("SHOW DATABASES")
    for x in cursor:
        print(x)


"""Delete Database"""


def deleteDatabase():
    name = input("Enter Database Name To delete: ")
    confirm = input("Are you sure you want to delete the database Y / N: ")
    if confirm.lower() == "y":
        cursor = myDatabase.cursor()
        cursor.execute("DROP DATABASE {}".format(name))
        print(name, "database was deleted successfully")
    else:
        print("Good Choice " + smile)


"""show all tables of database"""


def showTables():
    cursor = myDatabase.cursor()
    cursor.execute("SHOW TABLES")

    results = cursor.fetchall()
    if results is None:
        print("no table was created try to create one")
    else:
        for x in results:
            print(x)


"""Createing a table"""


def createTable():
    cursor = myDatabase.cursor()
    tableName = input("Enter Table Name: ")
    columnsNumber = int(input("How many columns you want to create: "))
    columns = []

    KeyQ = input("do you want to create primary key Y / N: ")
    if KeyQ.lower() == "y" or KeyQ.lower() == "yes":
        columnsNumber -= 1
        idName = input("Enter key name: ")
        columns.append(idName + " INT AUTO_INCREMENT PRIMARY KEY,")
    else:
        pass

    for col in range(columnsNumber):
        print("Enter column number %s" % (col + 1))
        name = input("column name: ")
        typ = input("column type: ")

        columns += name + ' ' + typ + ','

    query = ""
    for qu in columns:
        query += str(qu)

    query.startswith("(") and query.endswith(")")
    createQuery = "CREATE TABLE %s " % tableName + "(" + query[:-1] + ");"
    cursor.execute(createQuery)
    print("table created successfully\n")


"""Update specific record"""


def updateRecord():
    cursor = myDatabase.cursor()
    showTables()
    table = input("Choose table you want to update: ")
    print(getColumns(table))
    condition = input("By witch column you want to update: ")
    displayAllRecords(table)
    conditionValue = input(f"Choose the value of the {condition} you want to edit by: ")
    column = input("Which column you want to update: ")
    value = input(f"Enter the {column} you want to update to: ")

    query = f"UPDATE {table} SET {column} = {value} WHERE {condition} = {conditionValue}"
    cursor.execute(query)

    print(cursor.rowcount, "record(s) affected")


"""Show all Records in a specific table"""


def displayAllRecords(tableName):
    cursor = myDatabase.cursor()
    cursor.execute(f"SELECT * FROM {tableName}")
    result = cursor.fetchall()

    if result is None:
        print("table is empty try to add some records")
    else:
        for x in result:
            print(x)


"""get the columns names"""


def getColumns(tableName):
    cursor = myDatabase.cursor()
    cursor.execute(f"SHOW COLUMNS from {tableName};")

    lst = []
    for x in cursor.fetchall():
        lst.append(x[0])

    return lst


"""Select record by choice"""


def displaySpecificRecord():
    showTables()
    tableName = input("Enter table name: ")
    print(getColumns(tableName))
    column = input("Which column you want to get by: ")
    value = input(f"Enter a {column} you want to get by: ")

    cursor = myDatabase.cursor()
    cursor.execute(f"SELECT * FROM {tableName} WHERE {column} = {value}")

    result = cursor.fetchall()

    if result is None:
        print("table is empty try to add some records")
    else:
        for x in result:
            print(x)


"""deleting records"""


def removeRecord():
    cursor = myDatabase.cursor()
    showTables()
    table = input("choose a table: ")
    print(getColumns(table))
    condition = input("by witch column you want to delete: ")
    displayAllRecords(table)
    conditionValue = input(f"enter the {condition} of the record you want to delete: ")

    cursor.execute(f"DELETE FROM {table} WHERE {condition} = {conditionValue}")
    myDatabase.commit()
    print(cursor.rowcount, "record deleted")


"""deleting All records"""


def removeAllRecords():
    cursor = myDatabase.cursor()
    showTables()
    table = input("choose a table: ")
    q = input("Are you sure you want to delete all records Y / N: ")
    if q.lower() == "y" or q.lower() == 'yes':
        cursor.execute(f"DELETE * FROM {table}")
        myDatabase.commit()
        print(cursor.rowcount, "all records are deleted")
    else:
        print("good choice", smile)


"""Write you one query in the program"""


def writeQuery():
    cursor = myDatabase.cursor()
    showTables()
    query = input("write your query: ")
    cursor.execute(query)

    words = query.split()
    if words[0].lower() == 'select':
        for a in cursor.fetchall():
            print(a)
    else:
        myDatabase.commit()


"""Add new record"""


def insertRecords():
    cursor = myDatabase.cursor()
    showTables()
    table = input("which table you want to insert records to: ")

    columns = getColumns(table)
    columns.pop(0)

    n = int(input("how many records you want to insert: "))
    for nn in range(n):
        print(f"Enter record number {nn + 1}")
        colTxt = ""
        valuesTxt = ""
        for col in columns:
            value = input("Enter the value of %s" % col + ": ")
            colTxt += col + ","
            valuesTxt += value + ","
        cursor.execute(f"INSERT INTO {table} ({colTxt[:-1]}) VALUES ({valuesTxt[:-1]})")
        myDatabase.commit()

    print("record inserted.")


""" Showing Operations of tables after selecting the table"""


def useDatabase():
    statues = True
    showDatabases()
    databaseName = input("Choose database: ")
    myDatabase.connect(database=databaseName)
    while statues:
        tableMenu()
        print("You are connected to %s " % databaseName + "database")
        n = int(input("choose an operation: "))
        try:
            if n == 1:
                createTable()
            elif n == 2:
                insertRecords()
            elif n == 3:
                showTables()
            elif n == 4:
                updateRecord()
            elif n == 5:
                showTables()
                tableName = input("Enter table name: ")
                displayAllRecords(tableName)
            elif n == 6:
                displaySpecificRecord()
            elif n == 7:
                removeRecord()
            elif n == 8:
                removeAllRecords()
            elif n == 9:
                writeQuery()
            elif n == 10:
                statues = False
                print("___________ Thank You ___________")
            else:
                print("Wrong choice (^///^)")

        except Exception as e:
            print("\n", e, "\n")


"""Everything starts from this fucntion to show all the choices and all"""


def start():
    bol = True
    while bol:
        databaseMenu()
        choice = int(input("choose an operation: "))
        try:
            if choice == 1:
                createDatabase()
            elif choice == 2:
                showDatabases()
            elif choice == 3:
                useDatabase()
            elif choice == 4:
                deleteDatabase()
            elif choice == 5:
                bol = False
                print("___________ Thank You ___________")
            else:
                print("Wrong choice (^///^)")

        except Exception as e:
            print("\n", e, "\n")


def databaseMenu():
    print("      ¯\_(ツ)_/¯        WELCOME          ¯\_(ツ)_/¯      \n"
          "*********************************************************\n"
          "                     1)Create Database                   \n"
          "                     2)Show Database                     \n"
          "                     3)Use Database                      \n"
          "                     4)Drop Database                     \n"
          "                     5)exit                              \n"
          "*********************************************************")


def tableMenu():
    print("      ¯\_(ツ)_/¯        WELCOME          ¯\_(ツ)_/¯      \n"
          "*********************************************************\n"
          "                     1)create table                     \n"
          "                     2)insert records                   \n"
          "                     3)show tables                      \n"
          "                     4)update record                    \n"
          "                     5)show records of a table          \n"
          "                     6)show specific records            \n"
          "                     7)delete record                    \n"
          "                     8)delete all record                \n"
          "                     9)write your own Query             \n"
          "                     10)exit                             \n"
          "*********************************************************")


start()
