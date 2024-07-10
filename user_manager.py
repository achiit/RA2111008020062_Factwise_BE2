import json
import os
import datetime
from user_base import UserBase

class UserImpl(UserBase):
    def __init__(self):
        self.db_path = 'db/users.json'
        if not os.path.exists(self.db_path):
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            with open(self.db_path, 'w') as file:
                json.dump([], file)

    def create_user(self, request: str) -> str:
        try:
            if not request:
                raise ValueError("Request body is empty.")
            request_data = json.loads(request)
            print(request_data)
            name = request_data['name']
            display_name = request_data['display_name']

            if len(name) > 64 or len(display_name) > 64:
                raise ValueError("Name and display name must be max 64 characters.")

            with open(self.db_path, 'r') as file:
                users = json.load(file)

            for user in users:
                if user['name'] == name:
                    raise ValueError("User name must be unique.")

            user_id = (len(users) + 1)
            user = {
                "id": user_id,
                "name": name,
                "display_name": display_name,
                "creation_time": datetime.datetime.now().isoformat()
            }

            users.append(user)
            with open(self.db_path, 'w') as file:
                json.dump(users, file)

            return json.dumps({"id": user_id})
        except json.JSONDecodeError as jde:
            return json.dumps({"error": "Invalid JSON input", "details": str(jde)})
        except KeyError as ke:
            return json.dumps({"error": "Invalid input", "details": f"Missing key: {str(ke)}"})
        except ValueError as ve:
            return json.dumps({"error": str(ve)})

    def list_users(self) -> str:
        with open(self.db_path, 'r') as file:
            users = json.load(file)
        return json.dumps(users)

    def describe_user(self, request: str) -> str:
        request_data = json.loads(request)
        user_id = request_data['id']

        with open(self.db_path, 'r') as file:
            users = json.load(file)
            # print(users)

        for user in users:
            print("checking time")
            if user['id'] == user_id:
                print("now checking")
                return json.dumps(user)

        raise ValueError("user not found.")

    def update_user(self, request: str) -> str:
        try:
            if not request:
                raise ValueError("Request body is empty.")
            request_data = json.loads(request)
            user_id = request_data['id']
            updated_user = request_data['user']
            display_name = updated_user['display_name']

            if len(display_name) > 128:
                raise ValueError("Display name must be max 128 characters.")

            with open(self.db_path, 'r') as file:
                users = json.load(file)

            for user in users:
                if user['id'] == user_id:
                    user['display_name'] = display_name
                    with open(self.db_path, 'w') as file:
                        json.dump(users, file)
                    return json.dumps(user)

            return json.dumps({"error": "User not found"})
        except json.JSONDecodeError as jde:
            return json.dumps({"error": "Invalid JSON input", "details": str(jde)})
        except KeyError as ke:
            return json.dumps({"error": "Invalid input", "details": f"Missing key: {str(ke)}"})
        except ValueError as ve:
            return json.dumps({"error": str(ve)})

    def get_user_teams(self, request: str) -> str:
        try:
            if not request:
                raise ValueError("Request body is empty.")
            request_data = json.loads(request)
            user_id = request_data['id']

            with open('db/teams.json', 'r') as file:
                teams = json.load(file)

            user_teams = [team for team in teams if user_id in team['users']]

            return json.dumps(user_teams)
        except json.JSONDecodeError as jde:
            return json.dumps({"error": "Invalid JSON input", "details": str(jde)})
        except KeyError as ke:
            return json.dumps({"error": "Invalid input", "details": f"Missing key: {str(ke)}"})
        except ValueError as ve:
            return json.dumps({"error": str(ve)})
