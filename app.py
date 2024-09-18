from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

import main
import niche_management

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/tbgoennung'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        vorname=data['vorname'],
        name=data['name'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Login failed'}), 401


@app.route('/run_main', methods=['GET'])
def run_main():
    main.main()
    return "Main method executed successfully."


@app.route('/add_niche', methods=['POST'])
def add_niche():
    data = request.get_json()
    niche = data.get('niche')

    if niche:
        niche_management.add_task(niche)
        print(f"Niche '{niche}' added successfully.")
        return jsonify(message="Niche added successfully."), 200
    else:
        print("No 'niche' field in the provided data.")
        return jsonify(message="No 'niche' field in the provided data."), 400


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000)
