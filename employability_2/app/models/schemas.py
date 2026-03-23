from pydantic import BaseModel, Field


class TrainRequest(BaseModel):
    dataset: str = Field(default="set3")
    retrain_from_main: bool = Field(default=False)


class EvaluateRequest(BaseModel):
    test_dataset: str = Field(default="set1")


class ActivateVersionRequest(BaseModel):
    version_name: str


class DeployRequest(BaseModel):
    version_name: str | None = None


class DeleteVersionRequest(BaseModel):
    version_name: str
