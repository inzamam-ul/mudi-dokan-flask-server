
from bson.objectid import ObjectId
from flask import Flask, jsonify, request,Response
import flask
from flask_pymongo import PyMongo
from flask_cors import CORS
import json
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
dbname = os.getenv('DB_NAME')

app = Flask(__name__)
app.config['MONGO_URI'] = f'mongodb+srv://{user}:{password}@cluster0.gbf8e.mongodb.net/{dbname}?retryWrites=true&w=majority'

mongo = PyMongo(app)

CORS(app)

productCollection = mongo.db.products
orderCollection = mongo.db.orders

@app.route('/')
def index():
    return "Hello I'm PyMongo"

@app.route('/addProduct', methods=['POST'])
def addProduct():
    data = request.json
    print(data)
    product = {
        "name": request.json['name'],
        "imgUrl": request.json['imgUrl'],
        "price": request.json['price'],
        "weight": request.json['weight'],
    }
    dbresponse = productCollection.insert_one(product).inserted_id
    return jsonify(str(ObjectId(dbresponse)))


@app.route('/products', methods=['GET'])
def getProducts():

    data = list(productCollection.find())
    for pd in data:
        pd['_id'] = str(pd["_id"]),

    return Response(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )


@app.route('/singleProduct/<id>', methods=['GET'])
def getSingleProducts(id):
    
    data = list(productCollection.find({'_id': ObjectId(id)}))
    for pd in data:
        pd['_id'] = str(pd["_id"]),

    return Response(
        response=json.dumps(data[0]),
        status=200,
        mimetype='application/json'
    )



@app.route('/orders/<email>', methods=['GET'])
def getOrders(email):
    print(email)
    orders = list(orderCollection.find({"email" : email}))
    for order in orders:
        order['_id'] = str(order['_id'])
    return jsonify(orders)


@app.route('/updateProduct/<id>', methods=['PATCH'])
def updateProduct(id):
    print(request.json)
    productCollection.update_one(
        {"_id" : ObjectId(id)},
        {"$set" : {
            'name': request.json['name'],
            'imgUrl': request.json['imgUrl'],
            'price': request.json['price'],
            'weight': request.json['weight'],
        }}
    )
    return jsonify({'message': 'User Updated'})


@app.route('/deleteProduct/<id>', methods=['DELETE'])
def deleteOne(id):
    dbresponse = productCollection.delete_one({'_id' : ObjectId(id)})
    return jsonify(dbresponse.deleted_count>0)


if __name__ == '__main__':
    app.run(debug=True)