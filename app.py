import json
from flask import Flask, request, jsonify
from user_manager import UserImpl
from team_manager import TeamImpl
from project_board_manager import BoardImpl

app = Flask(__name__)
user_api = UserImpl()
team_api = TeamImpl()
board_api = BoardImpl()

@app.route('/user', methods=['POST'])
def create_user():
    try:
        response = user_api.create_user(json.dumps(request.json))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/users', methods=['GET'])
def list_users():
    try:
        response = user_api.list_users()
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/user/<int:user_id>', methods=['GET'])
def describe_user(user_id):
    try:
        print(user_id)
        response = user_api.describe_user(json.dumps({"id": user_id}))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user_data = request.json
        response = user_api.update_user(json.dumps({"id": user_id, "user": user_data}))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/user/<int:user_id>/teams', methods=['GET'])
def get_user_teams(user_id):
    try:
        response = user_api.get_user_teams(json.dumps({"id": user_id}))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/team', methods=['POST'])
def create_team():
    try:
        response = team_api.create_team(request.data.decode('utf-8'))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/teams', methods=['GET'])
def list_teams():
    try:
        response = team_api.list_teams()
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/team/<int:team_id>', methods=['GET'])
def describe_team(team_id):
    try:
        response = team_api.describe_team(json.dumps({"id": team_id}))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/team/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    try:
        team_data = request.json
        response = team_api.update_team(json.dumps({"id": team_id, "team": team_data}))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/team/<int:team_id>/users', methods=['POST'])
def add_users_to_team(team_id):
    try:
        users = request.json.get('users')
        response = team_api.add_users_to_team(json.dumps({"id": team_id, "users": users}))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/team/<int:team_id>/users', methods=['DELETE'])
def remove_users_from_team(team_id):
    try:
        users = request.json.get('users')
        response = team_api.remove_users_from_team(json.dumps({"id": team_id, "users": users}))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/team/<int:team_id>/users', methods=['GET'])
def list_team_users(team_id):
    try:
        response = team_api.list_team_users(json.dumps({"id": team_id}))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400
    
@app.route('/board', methods=['POST'])
def create_board():
    try:
        response = board_api.create_board(request.data.decode('utf-8'))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/board/<int:board_id>/close', methods=['POST'])
def close_board(board_id):
    try:
        response = board_api.close_board(json.dumps({"id": board_id}))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/board/<int:board_id>/task', methods=['POST'])
def add_task_to_board(board_id):
    try:
        task_data = request.json
        task_data['board_id'] = board_id
        response = board_api.add_task(json.dumps(task_data))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/task/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    try:
        status = request.json.get('status')
        response = board_api.update_task_status(json.dumps({"id": task_id, "status": status}))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/team/<int:team_id>/boards', methods=['GET'])
def list_boards(team_id):
    try:
        response = board_api.list_boards(json.dumps({"id": team_id}))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

@app.route('/board/<int:board_id>/export', methods=['GET'])
def export_board(board_id):
    try:
        response = board_api.export_board(json.dumps({"id": board_id}))
        return jsonify(json.loads(response))
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True)