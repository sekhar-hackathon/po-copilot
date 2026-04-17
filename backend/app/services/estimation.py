from typing import Dict

class Estimator:
    def __init__(self):
        # Initialize any necessary variables or models
        pass

    def suggest_effort(self, ticket_description: str) -> int:
        """
        Suggests an effort level for a given ticket description.
        Effort is measured in story points (1-5).
        """
        # Placeholder logic for effort estimation
        if 'complex' in ticket_description:
            return 5
        elif 'medium' in ticket_description:
            return 3
        else:
            return 1

    def suggest_priority(self, ticket_description: str) -> str:
        """
        Suggests a priority level for a given ticket description.
        Priority levels are 'High', 'Medium', 'Low'.
        """
        # Placeholder logic for priority estimation
        if 'urgent' in ticket_description:
            return 'High'
        elif 'important' in ticket_description:
            return 'Medium'
        else:
            return 'Low'

    def estimate(self, ticket_description: str) -> Dict[str, str]:
        """
        Provides both effort and priority estimation for a ticket.
        """
        return {
            'effort': self.suggest_effort(ticket_description),
            'priority': self.suggest_priority(ticket_description)
        }
