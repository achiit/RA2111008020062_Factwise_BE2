import json
import os
import datetime
from team_base import TeamBase

class TeamImpl(TeamBase):
    def __init__(self):
        self.db_path = 'db/teams.json'
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as file:
                json.dump([], file)

    def create_team(self, request: str) -> str:
        request_data = json.loads(request)
        name = request_data['name']
        description = request_data['description']
        admin = request_data['admin']

        if len(name) > 64 or len(description) > 128:
            raise ValueError("Name can be max 64 characters and description can be max 128 characters.")

        with open(self.db_path, 'r') as file:
            teams = json.load(file)

        for team in teams:
            if team['name'] == name:
                raise ValueError("Team name must be unique.")

        team_id = len(teams) + 1
        team = {
            "id": team_id,
            "name": name,
            "description": description,
            "admin": admin,
            "creation_time": datetime.datetime.now().isoformat()
        }

        teams.append(team)
        with open(self.db_path, 'w') as file:
            json.dump(teams, file)

        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        with open(self.db_path, 'r') as file:
            teams = json.load(file)
        return json.dumps(teams)

    def describe_team(self, request: str) -> str:
        request_data = json.loads(request)
        team_id = request_data['id']

        with open(self.db_path, 'r') as file:
            teams = json.load(file)

        for team in teams:
            if team['id'] == team_id:
                return json.dumps(team)

        raise ValueError("Team not found.")

    def update_team(self, request: str) -> str:
        request_data = json.loads(request)
        team_id = request_data['id']
        updated_team = request_data['team']
        name = updated_team['name']
        description = updated_team['description']
        admin = updated_team['admin']

        if len(name) > 64 or len(description) > 128:
            raise ValueError("Name can be max 64 characters and description can be max 128 characters.")

        with open(self.db_path, 'r') as file:
            teams = json.load(file)

        for team in teams:
            if team['id'] == team_id:
                team['name'] = name
                team['description'] = description
                team['admin'] = admin
                with open(self.db_path, 'w') as file:
                    json.dump(teams, file)
                return json.dumps(team)

        raise ValueError("Team not found.")

    def add_users_to_team(self, request: str):
        if request is None:
            raise ValueError("Invalid request format. Expecting JSON data.")

        try:
            request_data = json.loads(request)
            team_id = request_data['id']
            users_to_add = request_data['users']

            if len(users_to_add) > 50:
                raise ValueError("Cannot add more than 50 users at a time.")

            with open(self.db_path, 'r') as file:
                teams = json.load(file)

            team_found = False
            for team in teams:
                if team['id'] == team_id:
                    if 'users' not in team:
                        team['users'] = []

                    # Check if users are already added to the team
                    existing_users = set(team['users'])
                    users_to_add_set = set(users_to_add)

                    new_users = list(users_to_add_set - existing_users)
                    if not new_users:
                        return json.dumps({"message": "No new users added."})

                    team['users'].extend(new_users)
                    team_found = True
                    break

            if not team_found:
                raise ValueError("Team not found.")

            with open(self.db_path, 'w') as file:
                json.dump(teams, file)
            return json.dumps({"message":"users added successfully"})

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON input.")

        except KeyError as e:
            raise ValueError(f"Missing required field in request: {e}")

        except Exception as e:
            raise ValueError(f"An error occurred: {str(e)}")

    def remove_users_from_team(self, request: str):
        request_data = json.loads(request)
        team_id = request_data['id']
        users_to_remove = request_data['users']

        with open(self.db_path, 'r') as file:
            teams = json.load(file)

        for team in teams:
            if team['id'] == team_id:
                team['users'] = [user for user in team['users'] if user not in users_to_remove]
                with open(self.db_path, 'w') as file:
                    json.dump(teams, file)
                return json.dumps({"message": "users removed successfully"})

        raise ValueError("Team not found.")

    def list_team_users(self, request: str):
        request_data = json.loads(request)
        team_id = request_data['id']

        with open(self.db_path, 'r') as file:
            teams = json.load(file)

        for team in teams:
            if team['id'] == team_id:
                return json.dumps(team['users'])

        raise ValueError("Team not found.")
