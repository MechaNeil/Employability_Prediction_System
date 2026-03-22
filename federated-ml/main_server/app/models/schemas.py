from pydantic import BaseModel


class PredictRequest(BaseModel):
    records: list[dict[str, float]]
