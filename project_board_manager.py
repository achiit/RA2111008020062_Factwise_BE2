import json
import os
import datetime
from project_board_base import ProjectBoardBase

class BoardImpl(ProjectBoardBase):
    def __init__(self):
        self.db_path = 'db/boards.json'
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as file:
                json.dump([], file)

    def create_board(self, request: str):
        request_data = json.loads(request)
        name = request_data['name']
        description = request_data['description']
        team_id = request_data['team_id']

        if len(name) > 64 or len(description) > 128:
            raise ValueError("Name can be max 64 characters and description can be max 128 characters.")

        with open(self.db_path, 'r') as file:
            boards = json.load(file)

        for board in boards:
            if board['name'] == name and board['team_id'] == team_id:
                raise ValueError("Board name must be unique for a team.")

        board_id = len(boards) + 1
        board = {
            "id": board_id,
            "name": name,
            "description": description,
            "team_id": team_id,
            "creation_time": datetime.datetime.now().isoformat(),
            "status": "OPEN",
            "tasks": []
        }

        boards.append(board)
        with open(self.db_path, 'w') as file:
            json.dump(boards, file)

        return json.dumps({"id": board_id})

    def close_board(self, request: str) -> str:
        request_data = json.loads(request)
        board_id = request_data['id']

        with open(self.db_path, 'r') as file:
            boards = json.load(file)

        for board in boards:
            if board['id'] == board_id:
                if any(task['status'] != 'COMPLETE' for task in board['tasks']):
                    raise ValueError("Cannot close board with incomplete tasks.")
                board['status'] = 'CLOSED'
                board['end_time'] = datetime.datetime.now().isoformat()
                with open(self.db_path, 'w') as file:
                    json.dump(boards, file)
                return json.dumps(board)

        raise ValueError("Board not found.")

    def add_task(self, request: str) -> str:
        request_data = json.loads(request)
        title = request_data['title']
        description = request_data['description']
        user_id = request_data['user_id']
        board_id = request_data['board_id']

        if len(title) > 64 or len(description) > 128:
            raise ValueError("Title can be max 64 characters and description can be max 128 characters.")

        with open(self.db_path, 'r') as file:
            boards = json.load(file)

        for board in boards:
            if board['id'] == board_id:
                if board['status'] != 'OPEN':
                    raise ValueError("Can only add task to an OPEN board.")
                if any(task['title'] == title for task in board['tasks']):
                    raise ValueError("Task title must be unique for a board.")

                task_id = len(board['tasks']) + 1
                task = {
                    "id": task_id,
                    "title": title,
                    "description": description,
                    "user_id": user_id,
                    "creation_time": datetime.datetime.now().isoformat(),
                    "status": "OPEN"
                }

                board['tasks'].append(task)
                with open(self.db_path, 'w') as file:
                    json.dump(boards, file)

                return json.dumps({"id": task_id})

        raise ValueError("Board not found.")

    def update_task_status(self, request: str):
        request_data = json.loads(request)
        task_id = request_data['id']
        status = request_data['status']

        with open(self.db_path, 'r') as file:
            boards = json.load(file)

        for board in boards:
            for task in board['tasks']:
                if task['id'] == task_id:
                    task['status'] = status
                    with open(self.db_path, 'w') as file:
                        json.dump(boards, file)
                    return json.dumps(task)

        raise ValueError("Task not found.")

    def list_boards(self, request: str) -> str:
        request_data = json.loads(request)
        team_id = request_data['id']

        with open(self.db_path, 'r') as file:
            boards = json.load(file)

        team_boards = [board for board in boards if board['team_id'] == team_id and board['status'] == 'OPEN']

        return json.dumps(team_boards)

    def export_board(self, request: str) -> str:
        request_data = json.loads(request)
        board_id = request_data['id']

        with open(self.db_path, 'r') as file:
            boards = json.load(file)

        for board in boards:
            if board['id'] == board_id:
                out_file = f"out/board_{board_id}.txt"
                with open(out_file, 'w') as file:
                    file.write(f"Board Name: {board['name']}\n")
                    file.write(f"Description: {board['description']}\n")
                    file.write(f"Creation Time: {board['creation_time']}\n")
                    file.write(f"Status: {board['status']}\n")
                    file.write(f"Tasks:\n")
                    for task in board['tasks']:
                        file.write(f"  Task ID: {task['id']}\n")
                        file.write(f"  Title: {task['title']}\n")
                        file.write(f"  Description: {task['description']}\n")
                        file.write(f"  Assigned to: {task['user_id']}\n")
                        file.write(f"  Status: {task['status']}\n")
                        file.write(f"  Creation Time: {task['creation_time']}\n")
                        file.write("\n")

                return json.dumps({"out_file": out_file})

        raise ValueError("Board not found.")
