from pydantic import BaseModel

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
class WLSU(BaseModel):
    wlsu_id:str
    wlsu_name:str
    l1n1:str  
    cedetive_id:str
    wll:str
    sqi:str
    aqi:str
    vl:str
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