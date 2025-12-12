"""FastAPI entrypoint for IFCB focus metric service."""

import os

from stateless_microservice import ServiceConfig, create_app

from .processor import FocusProcessor

config = ServiceConfig(
    description="IFCB Focus metric microservice.",
)

DATA_DIR = os.getenv("DATA_DIR", "/data/ifcb")
MODEL_PATH = os.getenv("MODEL_PATH", "/models/slim_student_model.pkl")

app = create_app(FocusProcessor(data_dir=DATA_DIR, model_path=MODEL_PATH), config)
