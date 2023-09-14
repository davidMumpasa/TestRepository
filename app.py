from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3306/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy instance
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, email, name):
        self.email = email
        self.name = name

# Create the table in the database (you only need to do this once)
with app.app_context():
    db.create_all()

# Route to add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    
    new_user = User(name=username, email=email)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User added successfully"})

# Route to retrieve all users
@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.name,
            'email': user.email
        }
        user_list.append(user_data)
    
    return jsonify({"users": user_list})

if __name__ == '__main__':
    app.run(debug=True)
