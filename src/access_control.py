from typing import List, Dict

class User:
    def __init__(self, username: str, role: str, assigned_lines: List[str] = None):
        self.username = username
        self.role = role
        self.assigned_lines = assigned_lines if assigned_lines else []

class Machine:
    def __init__(self, machine_id: str, line: str):
        self.machine_id = machine_id
        self.line = line

class AccessControl:
    def __init__(self, users: List[User], machines: List[Machine]):
        self.users = {user.username: user for user in users}
        self.machines = machines

    def get_accessible_machines(self, username: str) -> List[Machine]:
        user = self.users.get(username)
        if not user:
            raise ValueError("User not found")

        if user.role == 'Plant Manager':
            return self.machines
        elif user.role == 'Operator':
            return [machine for machine in self.machines if machine.line in user.assigned_lines]
        else:
            return []
