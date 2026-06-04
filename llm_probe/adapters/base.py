from abc import ABC, abstractmethod
from llm_probe.schemas.result import Result
from llm_probe.schemas.payload import Payload


class BaseAdapter(ABC):
    """Abstract base for all LLM adapters.

    Every adapter must implement send() with this exact signature.
    The runner depends only on this interface, never on a concrete adapter.
    """

    def __init__(self, model: str, timeout: int = 30) -> None:
        self.model = model
        self.timeout = timeout

    @abstractmethod
    def send(self, payload: Payload) -> Result:
        """Send a single payload to the model and return a scored result.

        Args:
            payload: A validated Payload object from the catalog.

        Returns:
            A Result with the raw response and metadata filled in.
            Scoring fields are left for the scoring engine to populate.

        Raises:
            AdapterError: On any API or network failure.
        """