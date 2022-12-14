from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONs'] = False
#INIT db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

CORS(app)

# Product CLass/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String, nullable=True)

    def __init__(self, name, description, price, img_url):
        self.name = name
        self.description = description
        self.price = price
        self.img_url = img_url

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name','description', 'price', "img_url")

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create Product
@app.route('/add-product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    img_url = request.json.get("img_url")

    new_product = Product(name, description, price, img_url)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Get one products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Update Product
@app.route('/product/<id>', methods=['Put'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    img_url = request.json['img_url']

    product.name = name
    product.description = description
    product.price = price
    product.img_url = img_url

    db.session.commit()

    return product_schema.jsonify(product)

# Delete Product
@app.route('/product-del/<id>', methods=['DELETE'])
@cross_origin()
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

# Run server
if __name__ == '__main__':
    app.run(debug=True)