from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

class DataHistoryItem(BaseModel):
    timestamp: Optional[datetime] = None
    AQI: Optional[int] = None
    ISD: Optional[int] = None
    SQI: Optional[int] = None
    VL: Optional[int] = None
    WLL: Optional[int] = None

class WLSU(BaseModel):
    WLSU_ID: Optional[str] = None
    CLUSTER_ID: Optional[str | int] = None
    L1N1: Optional[list[str]] = None
    STATUS: Optional[bool] = None
    TIMESTAMP: Optional[datetime] = None
    WLSU_NAME: Optional[str] = None
    data_history: Optional[List[DataHistoryItem]] = None

    
class Zone(BaseModel):
    ZONE_ID : Optional[str] = None
    ZONE_NAME: Optional[str] = None
    CITY_ID: Optional[str] = None
    L1N1: Optional[list[int]] = None
    L2N2: Optional[list[int]] = None
    TIMESTAMP: Optional[datetime] = None
    STATUS: Optional[bool] = None

class Area(BaseModel):
    AREA_ID: Optional[str] = None
    AREA_NAME: Optional[str] = None
    ZONE_ID: Optional[str] = None
    L1N1: Optional[list[int]] = None
    L2N2: Optional[list[int]] = None
    TIMESTAMP:Optional[datetime] = None
    STATUS: Optional[bool] = None

class Cluster(BaseModel):
    CLUASTER_ID: Optional[str] = None
    AREA_ID: Optional[str] = None
    CEDATIVE_ID: Optional[str] = None
    CLUSTER_NAME: Optional[str] = None
    L1N1 : Optional[list[int]] = None
    L2N2: Optional[list[int]] = None
    ZONE_ID: Optional[str] = None
    CITY_ID: Optional[str] = None
    CEDATIVE_ID: Optional[str] = None
    TIMESTAMP:Optional[datetime] = None
    STATUS: Optional[bool] = None



class Cedative(BaseModel):
    CEDATIVE_ID: Optional[str] = None
    BACKUP_CEDATIVE_ID: Optional[str] = None
    L1N2: Optional[list[int]] = None
    BL1N2: Optional[list[int]] = None
    WLSU_ID: Optional[list[int]] = None
    CLUSTER_ID: Optional[str] = None
    TIMESTAMP: Optional[datetime] = None
    STATUS: Optional[bool] = None