"""IFCB Focus metric processor."""

import logging
from typing import List

import joblib
from pydantic import BaseModel, Field

from ifcb_focus import score_bin
from stateless_microservice import BaseProcessor, StatelessAction, run_blocking
from storage.utils import ReadonlyStore

from .bin_store import IFCBBinStore

logger = logging.getLogger(__name__)


class FocusMetricPathParams(BaseModel):
    """Path parameters for focus metric endpoint."""

    bin_id: str = Field(..., description="IFCB bin identifier (e.g., D20130823T160901_IFCB010)")


class FocusProcessor(BaseProcessor):
    """Processor for computing IFCB focus metrics."""

    def __init__(self, data_dir: str, model_path: str):
        super().__init__()

        # Initialize bin store
        logger.info(f"Initializing IFCB bin store with data_dir: {data_dir}")
        self.bin_store = ReadonlyStore(IFCBBinStore(data_dir))

        # Load the pre-trained focus model
        logger.info(f"Loading focus model from: {model_path}")
        self.model = joblib.load(model_path)
        logger.info("Focus model loaded successfully")

    @property
    def name(self) -> str:
        return "focus_metric"

    def get_stateless_actions(self) -> List[StatelessAction]:
        return [
            StatelessAction(
                name="focus_metric",
                path="/focus_metric/{bin_id}",
                path_params_model=FocusMetricPathParams,
                handler=self.handle_focus_metric,
                summary="Compute focus metric for an IFCB bin.",
                description="Returns the focus score for the specified IFCB bin.",
                tags=("focus",),
                media_type="text/plain",
                methods=("GET",),
            ),
        ]

    async def handle_focus_metric(self, path_params: FocusMetricPathParams):
        """Compute focus metric score for a bin.

        Args:
            path_params: Path parameters containing bin_id

        Returns:
            Focus score as string (text/plain)

        Raises:
            ValueError: If bin does not exist or data cannot be loaded
        """
        bin_id = path_params.bin_id

        # Check bin existence
        if not self.bin_store.exists(bin_id):
            raise ValueError(f"Bin {bin_id} not found in data directory")

        # Compute score in blocking context (I/O operations)
        score = await run_blocking(self._compute_score, bin_id)

        logger.info(f"Computed focus metric score for {bin_id}: {score:.4f}")

        return f"{score:.4f}"

    def _compute_score(self, bin_id: str) -> float:
        """Compute focus score for a bin.

        Args:
            bin_id: IFCB bin identifier

        Returns:
            Focus score (float)

        Raises:
            ValueError: If scoring fails
        """
        # Get bin data from bin store
        bin_data = self.bin_store.get(bin_id)

        # Call score_bin from ifcb-focus library
        score = score_bin(bin_data, self.model)

        return score
