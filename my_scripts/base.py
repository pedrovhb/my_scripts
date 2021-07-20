from abc import ABC

import fire


class Script(ABC):
    """Abstract base class for scripts that for now just provides a CLI
    interface through `fire`.
    """

    @classmethod
    def run(cls) -> None:
        """Entry point for CLI applications."""
        fire.Fire(cls)
