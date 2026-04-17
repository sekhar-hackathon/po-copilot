import unittest
from app.services.coding_assistant import CodingAssistant

class TestCodingAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = CodingAssistant(approved_ticket_types=['User Story', 'Task'])

    def test_propose_code_changes_approved(self):
        ticket = {'type': 'User Story', 'title': 'Repo-Aware Coding Assistant'}
        result = self.assistant.propose_code_changes(ticket)
        self.assertIn('Proposed code changes', result)

    def test_propose_code_changes_not_approved(self):
        ticket = {'type': 'Bug', 'title': 'Fix login issue'}
        result = self.assistant.propose_code_changes(ticket)
        self.assertEqual(result, 'Ticket type not approved for code proposals.')

if __name__ == '__main__':
    unittest.main()
