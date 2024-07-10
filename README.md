# Team Project Planner Tool

## Overview
The Team Project Planner Tool is a Python-based application designed to facilitate project management by providing APIs for managing users, teams, and tasks within a team board. It utilizes local file storage for persistence and is implemented using Flask for API development.

## Features

### User Management
- **Create User**: Allows creating a new user with unique username and display name.
- **List Users**: Retrieves a list of all users including their creation time.
- **Describe User**: Provides detailed information about a specific user based on user ID.
- **Update User**: Updates the display name of a user.

### Team Management
- **Create Team**: Creates a new team with a unique team name, description, and admin user.
- **List Teams**: Retrieves a list of all teams including their creation time and admin user.
- **Describe Team**: Provides detailed information about a specific team based on team ID.
- **Update Team**: Updates the name, description, and admin user of a team.
- **Add Users to Team**: Adds one or more users to a team, ensuring no duplicates are added and limiting to 50 users per request.
- **Remove Users from Team**: Removes one or more users from a team.

### Project Board Management
- **Create Board**: Creates a new project board for a team with a unique board name and description.
- **Close Board**: Marks a board as closed, ensuring all tasks are marked as complete.
- **Add Task to Board**: Adds a new task to a project board with a title, description, and assigned user.
- **Update Task Status**: Updates the status of a task to open, in progress, or complete.
- **List Boards**: Retrieves a list of all open boards for a specific team.
- **Export Board**: Creates a presentable view of a board and its tasks in a txt file.

## Persistence
The application uses local file storage (`db` folder) to persist data in JSON format:
- `users.json`: Stores user data.
- `teams.json`: Stores team data.
- `boards.json`: Stores project board data.

## Setup and Dependencies
To run the project, ensure you have Python installed along with the necessary libraries listed in `requirements.txt`. Install dependencies using:

```
pip3 install -r requirements.txt
```

# API Testing Guide Using Postman

## Prerequisites

1. **Install Postman:** Download and install Postman from Postman's website.
2. **Start Flask Server:** Ensure your Flask application is running (`python app.py`) to start the server locally.

## User Management

### Create User

- **Endpoint:** `POST /user`
- **Request Body:** JSON
  ```json
  {
    "name": "username",
    "display_name": "User Display Name"
  }
  ```
- **Expected Response:**
  ```json
  {
    "id": "<user_id>"
  }
  ```

### List Users

- **Endpoint:** `GET /users`
- **Expected Response:**
  ```json
  [
    {
      "name": "username",
      "display_name": "User Display Name",
      "creation_time": "YYYY-MM-DDTHH:MM:SS"
    }
  ]
  ```

### Describe User

- **Endpoint:** `GET /user/<user_id>`
- **Expected Response:**
  ```json
  {
    "name": "username",
    "display_name": "User Display Name",
    "creation_time": "YYYY-MM-DDTHH:MM:SS"
  }
  ```

### Update User

- **Endpoint:** `PUT /user/<user_id>`
- **Request Body:** JSON
  ```json
  {
    "user": {
      "display_name": "Updated Display Name"
    }
  }
  ```
- **Expected Response:**
  ```json
  {
    "id": "<user_id>",
    "name": "username",
    "display_name": "Updated Display Name",
    "creation_time": "YYYY-MM-DDTHH:MM:SS"
  }
  ```

## Team Management

### Create Team

- **Endpoint:** `POST /team`
- **Request Body:** JSON
  ```json
  {
    "name": "Team Name",
    "description": "Team Description",
    "admin": "<admin_user_id>"
  }
  ```
- **Expected Response:**
  ```json
  {
    "id": "<team_id>"
  }
  ```

### List Teams

- **Endpoint:** `GET /teams`
- **Expected Response:**
  ```json
  [
    {
      "name": "Team Name",
      "description": "Team Description",
      "creation_time": "YYYY-MM-DDTHH:MM:SS",
      "admin": "<admin_user_id>"
    }
  ]
  ```

### Describe Team

- **Endpoint:** `GET /team/<team_id>`
- **Expected Response:**
  ```json
  {
    "name": "Team Name",
    "description": "Team Description",
    "creation_time": "YYYY-MM-DDTHH:MM:SS",
    "admin": "<admin_user_id>"
  }
  ```

### Update Team

- **Endpoint:** `PUT /team/<team_id>`
- **Request Body:** JSON
  ```json
  {
    "team": {
      "name": "Updated Team Name",
      "description": "Updated Team Description",
      "admin": "<new_admin_user_id>"
    }
  }
  ```
- **Expected Response:**
  ```json
  {
    "id": "<team_id>",
    "name": "Updated Team Name",
    "description": "Updated Team Description",
    "creation_time": "YYYY-MM-DDTHH:MM:SS",
    "admin": "<new_admin_user_id>"
  }
  ```

### Add Users to Team

- **Endpoint:** `POST /team/<team_id>/users`
- **Request Body:** JSON
  ```json
  {
    "users": ["user_id1", "user_id2", ...]
  }
  ```
- **Expected Response:**
  ```json
  {
    "message": "Users added successfully."
  }
  ```

### Remove Users from Team

- **Endpoint:** `DELETE /team/<team_id>/users`
- **Request Body:** JSON
  ```json
  {
    "users": ["user_id1", "user_id2", ...]
  }
  ```
- **Expected Response:**
  ```json
  {
    "message": "Users removed successfully."
  }
  ```

### List Users of a Team

- **Endpoint:** `GET /team/<team_id>/users`
- **Expected Response:**
  ```json
  [
    {
      "id": "<user_id>",
      "name": "username",
      "display_name": "User Display Name"
    }
  ]
  ```

## Project Board Management

### Create Board

- **Endpoint:** `POST /board`
- **Request Body:** JSON
  ```json
  {
    "name": "Board Name",
    "description": "Board Description",
    "team_id": "<team_id>"
  }
  ```
- **Expected Response:**
  ```json
  {
    "id": "<board_id>"
  }
  ```

### Close Board

- **Endpoint:** `PUT /board/<board_id>/close`
- **Expected Response:**
  ```json
  {
    "message": "Board closed successfully."
  }
  ```

### Add Task to Board

- **Endpoint:** `POST /board/<board_id>/task`
- **Request Body:** JSON
  ```json
  {
    "title": "Task Title",
    "description": "Task Description",
    "user_id": "<user_id>"
  }
  ```
- **Expected Response:**
  ```json
  {
    "id": "<task_id>"
  }
  ```

### Update Task Status

- **Endpoint:** `PUT /task/<task_id>`
- **Request Body:** JSON
  ```json
  {
    "status": "IN_PROGRESS"
  }
  ```
- **Expected Response:**
  ```json
  {
    "id": "<task_id>",
    "status": "IN_PROGRESS"
  }
  ```

### List Boards

- **Endpoint:** `GET /boards/<team_id>`
- **Expected Response:**
  ```json
  [
    {
      "id": "<board_id>",
      "name": "Board Name"
    }
  ]
  ```

### Export Board

- **Endpoint:** `POST /board/<board_id>/export`
- **Expected Response:**
  - Download the exported board as a txt file.

