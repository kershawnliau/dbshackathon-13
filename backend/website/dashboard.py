from flask import Blueprint, request, jsonify
import json
from . import mysql

dashboard = Blueprint('dashboard', __name__)

class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return json.JSONEncoder.default(self, obj)

 

@dashboard.route('/dashboard', methods=["GET", "POST"])
def login():
    return "<h1> hello dashboard<h1>"

@dashboard.route('/getusers', methods=["GET", "POST"])
def getuser():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT UserID, Username, Firstname, Lastname, Email, Address FROM User")
    results = cursor.fetchall() 

    fields_list = cursor.description   # sql key name

    column_list = []
    for i in fields_list:
        column_list.append(i[0])

    jsonData_list = []
    for row in results:
        data_dict = {}
        for i in range(len(column_list)):
            data_dict[column_list[i]] = row[i]
        jsonData_list.append(data_dict)
    print("print final json data",jsonData_list)

    json_str = json.dumps(jsonData_list, cls=BytesEncoder)
    print(type(json_str))
    results = json_str.replace("\\","")
    print(results)
    return jsonify({"data": json_str, "code":200})



