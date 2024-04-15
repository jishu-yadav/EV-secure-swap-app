from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
from utility import generate_unique_id, get_date, sign_transaction, transmit_transaction, generateKeys
from collections import OrderedDict
EVDetailsModule
from transactionblock import blockchain, node_identifier
from blockchain import ElectricVehicle, RoadSideUnit, Blockchain
import datetime

=======
from blockchain import ElectricVehicle, RoadSideUnit, Blockchain
main

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


@app.route('/payments/<vehicleId>', methods=['GET'])
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

@app.route('/verify/<vehicleId>', methods=['GET'])
def verifyData(vehicleId):
     
     
     cur = mysql.connection.cursor()
     
     sql = 'SELECT v.vehicleId, v.vehicleName, v.ownerName, t.paymentId, t.lastBatterySwitch FROM transactions t JOIN vehicleinfo v ON t.vehicleId = v.vehicleId WHERE t.vehicleId = %s'
     


     cur.execute(sql,(vehicleId, ))
     column_metadata=cur.description
     column_names = [column[0] for column in column_metadata]
     data=cur.fetchone()
     res= OrderedDict(zip(column_names,data)) if data else {}
     transactionData = res  # Update the global transactionData variable with the fetched data
        
     
     # Convert datetime object to string format
     if 'lastBatterySwitch' in res and isinstance(transactionData['lastBatterySwitch'], datetime.datetime):
        transactionData['lastBatterySwitch'] = transactionData['lastBatterySwitch'].strftime('%Y-%m-%d %H:%M:%S')

     
     ev=ElectricVehicle(vehicleId)
     rsu_public_key = ev.public_key
  
     
     serialized_data, signature = ev.transmit_transaction_details(transactionData, rsu_public_key)

     rsu = RoadSideUnit(rsu_public_key)
     verified_transaction_details = rsu.verify_transaction(serialized_data, signature)

     if verified_transaction_details:
        blockchain = Blockchain()
        blockchain.add_block(verified_transaction_details)
     
     cur.close()
     return jsonify({'message': 'Data integrity verified.'})


#new blockchain


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'data']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['data'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        data="Reward for finding the proof",
    )
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    for node in nodes:
        blockchain.register_node(node)
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


if __name__=="__main__":
        app.run(host='127.1.1.1',debug=True)