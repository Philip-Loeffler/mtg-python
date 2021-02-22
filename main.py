import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/card')
def getCards():
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	try:
		cursor.execute("SELECT * FROM Card")
		rows = cursor.fetchall()
		res = jsonify(rows)
		res.status_code = 200
 
		return res
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/card/<int:id>')
def getCardById(id):
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	try:
		cursor.execute("SELECT * FROM card WHERE id={}".format(id))
		#fetchnone returns a single record or none if no more rows are available
		rows = cursor.fetchone() 
		res = jsonify(rows)
		res.status_code = 200

		return res
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()



#post
@app.route('/addCard', methods=['POST'])
def addCard():
	try:
		json = request.json
		ExpansionId = json.get("ExpansionID")
		cardName = json.get("Name")
		cardQuantity = json.get("Quantity")
		cardTypeId = json.get("TypeID")
		conn = mysql.connect()
		cursor = conn.cursor()
		sql = "INSERT INTO CARD (Name, Quantity, TypeID, ExpansionID) VALUES (cardName, cardQuantity, cardTypeId, ExpansionId)"
		cursor.execute(sql)
		conn.commit()
		resp = jsonify('card added successfully!')
		resp.status_code = 200

		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


# @app.route('/updateCard', methods=['PUT'])
# def updateCard():
# 		json = request.json
# 		ExpansionId = json.get("ExpansionID")
# 		cardName = json.get("Name")
# 		cardQuantity = json.get("Quantity")
# 		cardTypeId = json.get("TypeID")
# 		conn = mysql.connect()
# 		cursor = conn.cursor()
# 		sql = "INSERT INTO CARD (Name, Quantity, TypeID, ExpansionID) VALUES (cardName, cardQuantity, cardTypeId, ExpansionId)"
# 		cursor.execute(sql)
# 		conn.commit()
# 		resp = jsonify('card added successfully!')
# 		resp.status_code = 200

# 		return resp
# 	except Exception as e:
# 		print(e)
# 	finally:
# 		cursor.close() 
# 		conn.close()

@app.route('/deleteCard/<int:id>', methods=['DELETE'])
def deleteCard(id):
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	try:
		cursor.execute("DELETE FROM card WHERE id={}".format(id))
		conn.commit()
		#fetchnone returns a single record or none if no more rows are available
		res = jsonify('Employee deleted successfully!')
		res.status_code = 200
		return res

	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.errorhandler(404)
def not_found(error=None):
	    message = {
	        'status': 404,
	        'message': 'There is no record: ' + request.url,
	    }
	    res = jsonify(message)
	    res.status_code = 404

	    return res
			
if __name__ == "__main__":
	app.run()	