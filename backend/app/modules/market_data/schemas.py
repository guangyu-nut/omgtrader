from datetime import datetime

from pydantic import BaseModel


class DataSourceCreate(BaseModel):
    name: str
    provider_type: str
    enabled: bool = True


class DataSourceRead(BaseModel):
    id: str
    name: str
    provider_type: str
    enabled: bool

    model_config = {"from_attributes": True}


class DataSyncTaskRead(BaseModel):
    id: str
    data_source_config_id: str
    status: str
    started_at: datetime | None
    finished_at: datetime | None

    model_config = {"from_attributes": True}
