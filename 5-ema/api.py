from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend import User  # Import your User class

app = Flask(__name__)

# Create a SQLAlchemy database connection
engine = create_engine(
    "postgresql://rishabhmaniyar:90raWKtwUZBf@ep-square-wildflower-40600057.us-east-2.aws.neon.tech/karthik")
Session = sessionmaker(bind=engine)


# Define API routes for CRUD operations

@app.route('/users', methods=['GET'])
def get_users():
    # Retrieve all users
    session = Session()
    users = session.query(User).all()
    session.close()
    user_list = [{'user_id': user.user_id, 'username': user.username, 'phone': user.phone} for user in users]
    return jsonify({'users':user_list})


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Retrieve a specific user by user_id
    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()
    session.close()
    if user:
        return jsonify({'user_id': user.user_id, 'username': user.username, 'phone': user.phone})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/users', methods=['POST'])
def create_user():
    # Create a new user
    data = request.json
    new_user = User(username=data['username'], password=data['password'], phone=data['phone'], token=data['token'])
    session = Session()
    session.add(new_user)
    session.commit()
    session.close()
    return jsonify({'message': 'User created successfully'})


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Update an existing user
    data = request.json
    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        user.username = data['username']
        user.password = data['password']
        user.phone = data['phone']
        user.token = data['token']
        session.commit()
        session.close()
        return jsonify({'message': 'User updated successfully'})
    else:
        session.close()
        return jsonify({'message': 'User not found'}), 404


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Delete a user by user_id
    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        session.close()
        return jsonify({'message': 'User deleted successfully'})
    else:
        session.close()
        return jsonify({'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
