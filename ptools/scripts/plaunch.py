import webbrowser

from ptools.base import Script
from ptools.config import settings


class PLaunch(Script):
    """CLI for quickly getting into things."""

    @staticmethod
    def _ticket_from_digits(ticket_digits: str) -> str:
        """Given a digits-only string, return a ticket ID in the form DEF-123
        (if "DEF" is the configured default_jira_project_id).
        """
        project_id = settings.plaunch.jira_default_project_id
        if not project_id:
            raise ValueError("Default JIRA project not configured.")
        return f"{project_id}-{ticket_digits}"

    @classmethod
    def jira(cls, ticket_id: str) -> None:
        """Launch a browser tab for a JIRA ticket given its ID.

        If the provided ID is made up only of digits, it'll be transformed
        into a full ID using the default ticket prefix from settings.
        """
        ticket_id = str(ticket_id)
        if all(ch.isdigit() for ch in ticket_id):
            ticket_id = cls._ticket_from_digits(ticket_id)

        ticket_id = ticket_id.replace("_", "-")
        ticket_id = ticket_id.upper()

        print(f"Launching Jira issue {ticket_id} in new browser tab")
        base_url = settings.plaunch.jira_base_url.strip("/")
        webbrowser.open_new_tab(f"{base_url}/{ticket_id}")


if __name__ == "__main__":
    PLaunch.run()
