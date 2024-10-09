from fastapi import APIRouter,FastAPI,Request,HTTPException,Body
from fastapi.responses import JSONResponse
from config.db import get_dynamodb_resource
from fastapi.templating import Jinja2Templates
from models.GujcostModel import Zone,Area,WLSU,Cedative,Cluster
from typing import List
import datetime
from botocore.exceptions import ClientError
import json
AwsAPIRouter=APIRouter()
db=get_dynamodb_resource()
clusters_db = []
zones_db = []
areas_db = []
cedatives_db = []


# @AwsAPIRouter.post("/wlsu/", response_model=WLSU)
# async def create_wlsu(wlsu: WLSU):
#     """
#     Create a new WLSU in the database.

#     Args:
#         wlsu (WLSU): The WLSU to be created.

#     Returns:
#         dict: A dictionary with a message indicating success or failure.

#     Raises:
#         HTTPException: A 400 or 500 error if the request fails.
#     """    
#     try:
#         item = {
#             'WLSU_ID': wlsu.WLSU_ID,
#             'AQI': wlsu.AQI,
#             'CLUSTER_ID': wlsu.CLUSTER_ID,
#             'ISD': wlsu.ISD,
#             'L1N1': list(wlsu.L1N1),
#             'SQI': wlsu.SQI,
#             'STATUS': bool(wlsu.STATUS),
#             'TIMESTAMP': wlsu.TIMESTAMP.isoformat() if wlsu.TIMESTAMP else None,
#             'VL': wlsu.VL,
#             'WLL': wlsu.WLL,
#             'WLSU_NAME': wlsu.WLSU_NAME
#         }
#         db = get_dynamodb_resource()
#         wlsus_table = db.Table("WLSU")
#         result = wlsus_table.put_item(Item=item)
#         return {"message": "Inserted Successfully"}
#     except ClientError as e:
#         raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@AwsAPIRouter.post("/wlsu/", response_model=WLSU)
async def create_wlsu(wlsu: WLSU):
    """
    Create a new WLSU in the database.

    Args:
        wlsu (WLSU): The WLSU to be created.

    Returns:
        dict: A dictionary with a message indicating success or failure.

    Raises:
        HTTPException: A 400 or 500 error if the request fails.
    """
    try:
        # Convert `data_history` to the appropriate format for DynamoDB
        data_history = [
            {
                'timestamp': index.timestamp.isoformat() if index.timestamp else None,
                'AQI': str(index.AQI) if index.AQI is not None else None,
                'ISD': str(index.ISD) if index.ISD is not None else None,
                'SQI': str(index.SQI) if index.SQI is not None else None,
                'VL': str(index.VL) if index.VL is not None else None,
                'WLL': str(index.WLL) if index.WLL is not None else None
            }
            for index in wlsu.data_history
        ] if wlsu.data_history else []

        # Prepare the item to be inserted
        item = {
            'WLSU_ID': {'S': wlsu.WLSU_ID},
            'CLUSTER_ID': {'N': str(wlsu.CLUSTER_ID)} if wlsu.CLUSTER_ID is not None else None,
            'data_history': {'L': [{'M': dh} for dh in data_history]},
            'L1N1': {'L': [{'N': str(n)} for n in wlsu.L1N1]} if wlsu.L1N1 else [],
            'STATUS': {'BOOL': bool(wlsu.STATUS)},
            'TIMESTAMP': {'S': wlsu.TIMESTAMP.isoformat()} if wlsu.TIMESTAMP else None,
            'WLSU_NAME': {'S': wlsu.WLSU_NAME}
        }

        # Remove keys with None values (optional, but makes the DynamoDB record cleaner)
        item = {k: v for k, v in item.items() if v is not None}

        # Get DynamoDB resource and insert the item
        db = get_dynamodb_resource()
        wlsus_table = db.Table("WLSU")
        result = wlsus_table.put_item(Item=item)

        return {"message": "Inserted Successfully"}

    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# # Get all WLSUs
@AwsAPIRouter.get("/wlsus/", response_model=List[WLSU])
async def get_wlsus():
    db = get_dynamodb_resource()
    wlsus_table = db.Table("WLSU")
    try:
        result = wlsus_table.scan()
        items = result.get('Items', [])
        while 'LastEvaluatedKey' in result:
            result = wlsus_table.scan(ExclusiveStartKey=result['LastEvaluatedKey'])
            items.extend(result.get('Items', []))
        return items
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
# Get WLSU by ID
@AwsAPIRouter.get("/wlsus/{wlsu_id}", response_model=WLSU)
async def get_wlsu(wlsu_id: str):
    db = get_dynamodb_resource()
    wlsus_table = db.Table("WLSU")
    try:
        response = wlsus_table.get_item(Key={"WLSU_ID":wlsu_id})
        item = response.get('Item')
        if item is None:
            raise HTTPException(status_code=404, detail="WLSU not found")
        return item
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
# Update WLSU by ID
@AwsAPIRouter.put("/wlsus/{wlsu_id}", response_model=WLSU)
async def update_wlsu(wlsu_id: str, updated_wlsu: WLSU):
    db = get_dynamodb_resource()
    wlsus_table = db.Table("WLSU")
    response = wlsus_table.delete_item(Key={'itemId': wlsu_id})
    return response

# Delete WLSU by ID
@AwsAPIRouter.delete("/wlsus/{wlsu_id}")
async def delete_wlsu(wlsu_id: str):
    db = get_dynamodb_resource()
    wlsus_table = db.Table("WLSU")
    try:
        response = wlsus_table.delete_item(Key={"WLSU_ID": wlsu_id})
        if response.get('Attributes') is None:
            raise HTTPException(status_code=404, detail="WLSU not found")
        return {"message": "WLSU deleted successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])

@AwsAPIRouter.get("/",response_class=JSONResponse)
async def add_zone(request:Request):
    return {"Hello":"World"}

# Create a new zone
@AwsAPIRouter.post("/zones/", response_model=Zone)
async def create_zone(zone: Zone):
    # Generate a unique ID for the zone
    zone.zone_id = str(datetime.datetime.now())
    zones_db.append(zone)
    return zone

# Get all zones
@AwsAPIRouter.get("/zones/", response_model=List[Zone])
async def get_zones():
    return zones_db

# Get a zone by ID
@AwsAPIRouter.get("/zones/{zone_id}", response_model=Zone)
async def get_zone(zone_id: str):
    for zone in zones_db:
        if zone.zone_id == zone_id:
            return zone
    raise HTTPException(status_code=404, detail="Zone not found")

# Update a zone by ID
@AwsAPIRouter.put("/zones/{zone_id}", response_model=Zone)
async def update_zone(zone_id: str, updated_zone: Zone):
    for i, zone in enumerate(zones_db):
        if zone.zone_id == zone_id:
            zones_db[i] = updated_zone
            zones_db[i].zone_id = zone_id  # Ensure the ID remains the same
            return zones_db[i]
    raise HTTPException(status_code=404, detail="Zone not found")

# Delete a zone by ID
@AwsAPIRouter.delete("/zones/{zone_id}")
async def delete_zone(zone_id: str):
    for i, zone in enumerate(zones_db):
        if zone.zone_id == zone_id:
            del zones_db[i]
            return {"detail": "Zone deleted"}
    raise HTTPException(status_code=404, detail="Zone not found")
# Create Cedative
@AwsAPIRouter.post("/cedatives/", response_model=Cedative)
async def create_cedative(cedative: Cedative):
    cedative.cedative_id = str(uuid4())
    cedatives_db.append(cedative)
    return cedative

# Get all Cedatives
@AwsAPIRouter.get("/cedatives/", response_model=List[Cedative])
async def get_cedatives():
    return cedatives_db

# Get Cedative by ID
@AwsAPIRouter.get("/cedatives/{cedative_id}", response_model=Cedative)
async def get_cedative(cedative_id: str):
    for cedative in cedatives_db:
        if cedative.cedative_id == cedative_id:
            return cedative
    raise HTTPException(status_code=404, detail="Cedative not found")

# Update Cedative by ID
@AwsAPIRouter.put("/cedatives/{cedative_id}", response_model=Cedative)
async def update_cedative(cedative_id: str, updated_cedative: Cedative):
    for i, cedative in enumerate(cedatives_db):
        if cedative.cedative_id == cedative_id:
            cedatives_db[i] = updated_cedative
            cedatives_db[i].cedative_id = cedative_id
            return cedatives_db[i]
    raise HTTPException(status_code=404, detail="Cedative not found")

# Delete Cedative by ID
@AwsAPIRouter.delete("/cedatives/{cedative_id}")
async def delete_cedative(cedative_id: str):
    for i, cedative in enumerate(cedatives_db):
        if cedative.cedative_id == cedative_id:
            del cedatives_db[i]
            return {"detail": "Cedative deleted"}
    raise HTTPException(status_code=404, detail="Cedative not found")

# Create Cluster
@AwsAPIRouter.post("/clusters/", response_model=Cluster)
async def create_cluster(cluster: Cluster):
    cluster.cluster_id = str(uuid4())
    clusters_db.append(cluster)
    return cluster

# Get all Clusters
@AwsAPIRouter.get("/clusters/", response_model=List[Cluster])
async def get_clusters():
    return clusters_db

# Get Cluster by ID
@AwsAPIRouter.get("/clusters/{cluster_id}", response_model=Cluster)
async def get_cluster(cluster_id: str):
    for cluster in clusters_db:
        if cluster.cluster_id == cluster_id:
            return cluster
    raise HTTPException(status_code=404, detail="Cluster not found")

# Update Cluster by ID
@AwsAPIRouter.put("/clusters/{cluster_id}", response_model=Cluster)
async def update_cluster(cluster_id: str, updated_cluster: Cluster):
    for i, cluster in enumerate(clusters_db):
        if cluster.cluster_id == cluster_id:
            clusters_db[i] = updated_cluster
            clusters_db[i].cluster_id = cluster_id
            return clusters_db[i]
    raise HTTPException(status_code=404, detail="Cluster not found")

# Delete Cluster by ID
@AwsAPIRouter.delete("/clusters/{cluster_id}")
async def delete_cluster(cluster_id: str):
    for i, cluster in enumerate(clusters_db):
        if cluster.cluster_id == cluster_id:
            del clusters_db[i]
            return {"detail": "Cluster deleted"}
    raise HTTPException(status_code=404, detail="Cluster not found")


@AwsAPIRouter.post("/areas/", response_model=Area)
async def create_area(area: Area):
    area.area_id = str(uuid4())
    areas_db.append(area)
    return area

@AwsAPIRouter.get("/areas/", response_model=List[Area])
async def get_areas():
    return areas_db

@AwsAPIRouter.get("/areas/{area_id}", response_model=Area)
async def get_area(area_id: str):
    for area in areas_db:
        if area.area_id == area_id:
            return area
    raise HTTPException(status_code=404, detail="Area not found")

@AwsAPIRouter.put("/areas/{area_id}", response_model=Area)
async def update_area(area_id: str, updated_area: Area):
    for i, area in enumerate(areas_db):
        if area.area_id == area_id:
            areas_db[i] = updated_area
            areas_db[i].area_id = area_id
            return areas_db[i]
    raise HTTPException(status_code=404, detail="Area not found")

@AwsAPIRouter.delete("/areas/{area_id}")
async def delete_area(area_id: str):
    for i, area in enumerate(areas_db):
        if area.area_id == area_id:
            del areas_db[i]
            return {"detail": "Area deleted"}
    raise HTTPException(status_code=404, detail="Area not found")


@AwsAPIRouter.get("/RouteData")
async def find_route_data(route_data: dict = Body(...)):
    turning_points = [(float(point['latitude']), float(point['longitude'])) for point in route_data['turning_points']]
    wlsus_list=list(get_wlsus())
    data={}
    for i in range(0,len(turning_points)-1):
        loc1=turning_points[0]
        loc2=turning_points[1]
        for wlsu in wlsus_list:
            wlsu_cordinates=wlsu.get("L1N1")
            if (loc1[0]<=wlsu_cordinates[0]<=loc2[0])and(loc1[1]<=wlsu_cordinates[1]<=loc2[1]):
                data[i]=list(wlsu.get("data_hisory"))[0]
    return data

 