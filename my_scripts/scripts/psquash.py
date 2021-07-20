from typing import Dict, Final

import httpx

from my_scripts.base import Script
from my_scripts.config import settings


class PSquash(Script):
    """CLI for squash.io VM info.

    Get information related to Squash.io deployment VMs.
    todo: implement a proper authentication flow. At the moment I just take
     the session ID from the browser.
    """

    _INSTANCES_URL: Final[str] = "https://app.squash.io/api/vm-list/"

    _QUERY_STRING: Final[Dict[str, str]] = {
        "user_pk": settings.psquash.squash_user_pk,
        "status_str": "running",
        "organization_pk": settings.psquash.squash_organization_pk,
    }
    _HEADERS: Final[Dict[str, str]] = {
        "Cookie": f"sessionid={settings.psquash.squash_session_id}"
    }

    def _get_instances(self) -> dict:
        response = httpx.get(
            self._INSTANCES_URL,
            headers=self._HEADERS,
            params=self._QUERY_STRING,
        )
        response.raise_for_status()
        data = response.json()
        assert isinstance(data, dict)
        return data

    def _build_ssh_str(self, result: dict) -> str:
        ip = result["ip_address"]
        port = result["ssh_port"]
        return f"ssh -p {port} test-instance@{ip}"

    def instances(self) -> dict:
        return self._get_instances()

    def deployment_ips(self) -> Dict[str, str]:
        instances = self._get_instances()
        return {
            result["deployment"]["get_name"]: result["ip_address"]
            for result in instances["results"]
        }

    def deployment_ssh(self) -> Dict[str, str]:
        instances = self._get_instances()
        return {
            result["deployment"]["get_name"]: self._build_ssh_str(result)
            for result in instances["results"]
        }

    def ip_for(self, branch: str) -> str:
        return self.deployment_ips()[branch]

    def ssh_for(self, branch: str) -> str:
        """Get the command that starts a session in the VM for the given branch.

        $ psquash ssh_for staging_branch
          ssh -p 41896 test-instance@50.133.33.37
        """
        return self.deployment_ssh()[branch]


if __name__ == "__main__":
    PSquash.run()
