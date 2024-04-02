from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
from utility import generate_unique_id, get_date
from collections import OrderedDict

app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ev'

mysql = MySQL(app)

@app.route("/")
def home():
    return "Home"

@app.route("/vehicleInfo",methods=['POST'])
def setVehicleInfo():
      vehicleId=generate_unique_id()
      vname=request.json['vehicleName']
      ownerName=request.json['ownerName']
      purchaseDate=get_date()

      cur = mysql.connection.cursor()
      cur.execute('''INSERT INTO vehicleInfo (vehicleId,vehicleName, ownerName,purchaseDate) VALUES (%s,%s, %s, %s)''', (vehicleId, vname, ownerName, purchaseDate))
      mysql.connection.commit()
      cur.close()
      return jsonify({'message': 'Data added successfully'})

 
@app.route("/customers/<name>",methods=['GET'])
def getCustomerDetails(name):
      cur = mysql.connection.cursor()
      name_pattern = '%' + name + '%'
      cur.execute('''SELECT * FROM vehicleInfo WHERE ownerName LIKE %s''',(name_pattern,))

      data=cur.fetchall()
      cur.close()
      return jsonify(data)




@app.route('/transactions/<vehicleId>', methods=['POST'])
def add_or_edit_timestamp(vehicleId):
    # Receive data from request
    cur = mysql.connection.cursor()
    vID = vehicleId
    paymentID = generate_unique_id()
    timestamp = get_date()

    try:
        # Check if entry with vehicleId exists
        sql = "SELECT * FROM transactions WHERE vehicleID = %s"
        cur.execute(sql, (vID,))
        result = cur.fetchone()

        if result:
            # If entry exists, update the timestamp
            sql = "UPDATE transactions SET lastBatterySwitch = %s, paymentID = %s WHERE vehicleID = %s"
            cur.execute(sql, (timestamp, paymentID, vID))
        else:
            # If entry doesn't exist, insert new row
            sql = "INSERT INTO transactions (vehicleID, paymentID, lastBatterySwitch) VALUES (%s, %s, %s)"
            cur.execute(sql, (vID, paymentID, timestamp))

        mysql.connection.commit()
        return jsonify({'message': 'Data added/updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/payment/<vehicleId>', methods=['GET'])
def getTransactionData(vehicleId):
     cur = mysql.connection.cursor()
     
     sql = 'SELECT v.vehicleId, v.vehicleName, v.ownerName, t.paymentId, t.lastBatterySwitch FROM transactions t JOIN vehicleinfo v ON t.vehicleId = v.vehicleId WHERE t.vehicleId = %s'
     


     cur.execute(sql,(vehicleId, ))
     column_metadata=cur.description
     column_names = [column[0] for column in column_metadata]
     data=cur.fetchone()
     res= OrderedDict(zip(column_names,data)) if data else {}
     cur.close()
     return jsonify(res)

if __name__=="__main__":
        app.run(host='127.1.1.1',debug=True)