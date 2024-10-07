from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WLSU(BaseModel):
    WLSU_ID: Optional[str] = None
    AQI: Optional[int] = None
    CLUSTER_ID: Optional[str | int] = None
    ISD: Optional[int] = None
    L1N1: Optional[list[int]] = None
    SQI: Optional[int] = None
    STATUS: Optional[bool] = None
    TIMESTAMP: Optional[datetime] = None
    VL: Optional[int] = None
    WLL: Optional[int] = None
    WLSU_NAME: Optional[str] = None
    
class Zone(BaseModel):
    zone_id:str
    zone_name:str
    city_id:str
    l1n2:str
    l2n2:str
    timestamp:str
    status:str

class Area(BaseModel):
    area_id:str
    area_name:str
    zone_id:str
    l1n2:str
    l2n2:str
    timestamp:str
    status:str

class Cluster(BaseModel):
    cluster_id:str
    cluster_name:str
    l1n1:str
    zone_id:str
    city_id:str
    cedetive_id:str
    timestamp:str
    status:str



class Cedative(BaseModel):
    cedative_id:str
    bl1n1:str  
    bcedativeid:str
    wlsu_id:str
    cluster_id:str
    timestamp:str
    status:str