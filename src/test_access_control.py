import unittest
from access_control import User, Machine, AccessControl

class TestAccessControl(unittest.TestCase):
    def setUp(self):
        self.machines = [
            Machine(machine_id='M1', line='Line1'),
            Machine(machine_id='M2', line='Line2'),
            Machine(machine_id='M3', line='Line3')
        ]
        self.users = [
            User(username='manager', role='Plant Manager'),
            User(username='operator1', role='Operator', assigned_lines=['Line1']),
            User(username='operator2', role='Operator', assigned_lines=['Line2'])
        ]
        self.access_control = AccessControl(users=self.users, machines=self.machines)

    def test_plant_manager_access(self):
        accessible_machines = self.access_control.get_accessible_machines('manager')
        self.assertEqual(len(accessible_machines), 3)

    def test_operator_access(self):
        accessible_machines_op1 = self.access_control.get_accessible_machines('operator1')
        self.assertEqual(len(accessible_machines_op1), 1)
        self.assertEqual(accessible_machines_op1[0].machine_id, 'M1')

        accessible_machines_op2 = self.access_control.get_accessible_machines('operator2')
        self.assertEqual(len(accessible_machines_op2), 1)
        self.assertEqual(accessible_machines_op2[0].machine_id, 'M2')

    def test_invalid_user(self):
        with self.assertRaises(ValueError):
            self.access_control.get_accessible_machines('nonexistent')

if __name__ == '__main__':
    unittest.main()
