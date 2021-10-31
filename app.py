from logging import debug
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["DATABASE_URL"] = "mysql://bb2ef251680853:f96c55a9@us-cdbr-east-04.cleardb.com/heroku_b1238e369440257?"

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Decimal, nullable=False)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "first_name", "last_name")

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

class AdminSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "first_name", "last_name")

admin_schema = AdminSchema()
multiple_admin_schema = AdminSchema(many=True)

class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "price")

product_schema = ProductSchema()
multiple_product_schema = ProductSchema(many=True)


@app.route("/user/add", methods=["POST"])
def add_user():
    if request.content_type != "application/json":
        return jsonify("Error, Data must be sent as JSON")
    
    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")
    first_name = post_data.get("first_name")
    last_name = post_data.get("last_name")

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_record = User(username, pw_hash, first_name, last_name)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(user_schema.dump(new_record))

@app.route("/user/get/<id>", methods=["GET"])
def get_user(id):
    user = db.session.query(User).filter(User.id == id).first()
    return jsonify(user_schema.dump(user))

@app.route("/user/get", methods=["GET"])
def get_all_users():
    all_users = db.session.query(User).all()
    return jsonify(multiple_user_schema.dump(all_users))

@app.route("/user/get/<username>", methods=["GET"])
def get_user(username):
    user = db.session.query(User).filter(User.username == username).first()
    return jsonify(user_schema.dump(user))

@app.route("/user/get/<password>", methods=["GET"])
def get_user2(password):
    user = db.session.query(User).filter(User.password == password).first()
    return jsonify(user_schema.dump(user))

@app.route("/user/get/<first_name>", methods=["GET"])
def get_user3(first_name):
    user = db.session.query(User).filter(User.first_name == first_name).first()
    return jsonify(user_schema.dump(user))

@app.route("/user/get/<last_name>", methods=["GET"])
def get_user3(last_name):
    user = db.session.query(User).filter(User.last_name == last_name).first()
    return jsonify(user_schema.dump(user))

@app.route("/user/verification", methods=["POST"])
def verification():
    if request.content_type != "application/json":
        return jsonify("Error, Data must be sent as JSON")
    
    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    user = db.session.query(User).filter(User.username == username).first()

    if user is None:
        return jsonify("User NOT Verified")
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify("User NOT Verified")
    
    return jsonify("User Verified")

@app.route("/user/update/<id>", methods=["PUT"])
def update_user(id):
    if request.content_type != "application/json":
        return jsonify("Error, Data must be sent as JSON")
    
    put_data = request.get_json()

    user = db.session.query(User).filter(User.id == id).first()

    db.session.commit()


@app.route("/admin/add", methods=["POST"])
def add_admin():
    if request.content_type != "application/json":
        return jsonify("Error, Data must be sent as JSON")
    
    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")
    first_name = post_data.get("first_name")
    last_name = post_data.get("last_name")

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_record = Admin(username, pw_hash, first_name, last_name)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(user_schema.dump(new_record))

@app.route("/admin/get/<id>", methods=["GET"])
def get_admin(id):
    admin = db.session.query(Admin).filter(Admin.id == id).first()
    return jsonify(admin_schema.dump(admin))

@app.route("/admin/get", methods=["GET"])
def get_all_admins():
    all_admins = db.session.query(Admin).all()
    return jsonify(multiple_admin_schema.dump(all_admins))

@app.route("/admin/get/<username>", methods=["GET"])
def get_admin(username):
    admin = db.session.query(Admin).filter(Admin.username == username).first()
    return jsonify(admin_schema.dump(admin))

@app.route("/admin/get/<password>", methods=["GET"])
def get_admin2(password):
    admin = db.session.query(Admin).filter(Admin.password == password).first()
    return jsonify(admin_schema.dump(admin))

@app.route("/admin/get/<first_name>", methods=["GET"])
def get_admin3(first_name):
    admin = db.session.query(Admin).filter(Admin.first_name == first_name).first()
    return jsonify(admin_schema.dump(admin))

@app.route("/admin/get/<last_name>", methods=["GET"])
def get_admin3(last_name):
    admin = db.session.query(Admin).filter(Admin.last_name == last_name).first()
    return jsonify(admin_schema.dump(admin))

@app.route("/admin/verification", methods=["POST"])
def verification():
    if request.content_type != "application/json":
        return jsonify("Error, Data must be sent as JSON")
    
    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    admin = db.session.query(Admin).filter(Admin.username == username).first()

    if admin is None:
        return jsonify("Admin NOT Verified")
    
    if not bcrypt.check_password_hash(admin.password, password):
        return jsonify("Admin NOT Verified")
    
    return jsonify("Admin Verified")

@app.route("/admin/update/<id>", methods=["PUT"])
def update_admin(id):
    if request.content_type != "application/json":
        return jsonify("Error, Data must be sent as JSON")
    
    put_data = request.get_json()

    admin = db.session.query(Admin).filter(Admin.id == id).first()

    db.session.commit()














@app.route("/product/add", methods=["POST"])
def add_info():
    if request.content_type != "application/json":
        return jsonify("Error, Data must be sent as JSON")
    post_data = request.get_json()
    name = post_data.get("name")
    description = post_data.get("description")
    price = post_data.get("price")

    new_record = Product(name, description, price)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(product_schema.dump(new_record))

@app.route("/product/get", methods=["GET"])
def get_all_products():
    all_products = db.session.query(Product).all()
    return jsonify(multiple_product_schema.dump(all_products))

@app.route("/product/get/<name>", methods=["GET"])
def get_product(name):
    product = db.session.query(Product).filter(Product.name == name).first()
    return jsonify(product_schema.dump(product))

@app.route("/product/get/<description>", methods=["GET"])
def get_product2(description):
    product = db.session.query(Product).filter(Product.description == description).first()
    return jsonify(product_schema.dump(product))

@app.route("/product/get/<price>", methods=["GET"])
def get_product3(price):
    product = db.session.query(Product).filter(Product.price == price).first()
    return jsonify(product_schema.dump(product))

@app.route("/product/delete/<user_id>", methods=["DELETE"])
def delete_infos(user_id):
    infos = db.session.query(Info).filter(Info.user_id == user_id).all()
    for info in infos:
        db.session.delete(info)
        db.session.commit()
    user = db.session.query(User).filter(User.id == user_id).first()
    return jsonify(user_schema.dump(user))


if __name__ == "__main__":
    app.run(debug=True)