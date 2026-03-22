from pydantic import BaseModel
from pydantic import Field


class PredictRequest(BaseModel):
    records: list[dict[str, float]]


class RemoteUploadMeta(BaseModel):
    source_server: str
    target_server: str
    model_family: str


class TrainMainRequest(BaseModel):
    dataset: str = Field(default="set1")


class RetrainTargetsRequest(BaseModel):
    targets: list[str] = Field(default_factory=lambda: ["hospital_1", "hospital_2"])
    dataset: str = Field(default="set2")


class VersionCompareItem(BaseModel):
    label: str
    model_family: str
    version_name: str


class VersionCompareRequest(BaseModel):
    test_dataset: str = Field(default="set1")
    items: list[VersionCompareItem]
