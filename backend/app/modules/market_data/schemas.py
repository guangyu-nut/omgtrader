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


class DataCoverageRead(BaseModel):
    symbol_code: str
    daily_start: datetime | None = None
    daily_end: datetime | None = None
    minute_start: datetime | None = None
    minute_end: datetime | None = None

    model_config = {"from_attributes": True}
