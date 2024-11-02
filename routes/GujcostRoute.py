from fastapi import APIRouter,Request,HTTPException,Body
from fastapi.responses import JSONResponse
from config.db import get_dynamodb_resource
from models.GujcostModel import Zone,Area,WLSU,Cedative,Cluster,DataHistoryItem
from typing import List
from botocore.exceptions import ClientError
from fastapi.encoders import jsonable_encoder

AwsAPIRouter=APIRouter()
db=get_dynamodb_resource()

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
        data_history = [
            {
                'timestamp': index.timestamp.isoformat() if index.timestamp else {'NULL': True},
                'AQI': index.AQI if index.AQI is not None else {'NULL': True},
                'ISD': index.ISD if index.ISD is not None else {'NULL': True},
                'SQI': index.SQI if index.SQI is not None else {'NULL': True},
                'VL': index.VL if index.VL is not None else {'NULL': True},
                'WLL': index.WLL if index.WLL is not None else {'NULL': True}
            }
            for index in wlsu.data_history
        ] if wlsu.data_history else []
        
        item = {
            'WLSU_ID': wlsu.WLSU_ID,
            'CLUSTER_ID': wlsu.CLUSTER_ID if wlsu.CLUSTER_ID is not None else {'NULL': True},
            'data_history': [dh for dh in data_history],
            'L1N1': [ n for n in wlsu.L1N1],
            'STATUS': wlsu.STATUS,
            'TIMESTAMP': wlsu.TIMESTAMP.isoformat() if wlsu.TIMESTAMP else {'NULL': True},
            'WLSU_NAME': wlsu.WLSU_NAME
        }
        db = get_dynamodb_resource()
        wlsus_table = db.Table("WLSU")
        wlsus_table.put_item(Item=item)
        return {"message": "Inserted Successfully"}

    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@AwsAPIRouter.put("/datahistory/{wlsu_id}", response_model=DataHistoryItem)
async def add_data(wlsu_id: str, datahistory: DataHistoryItem):
    data_history = {
        'timestamp': datahistory.timestamp.isoformat() if datahistory.timestamp else None,
        'AQI': datahistory.AQI,
        'ISD': datahistory.ISD,
        'SQI': datahistory.SQI,
        'VL': datahistory.VL,
        'WLL': datahistory.WLL
    }

    db = get_dynamodb_resource()
    wlsus_table = db.Table("WLSU")

    try:
        # Fetch existing item to ensure it exists
        response = wlsus_table.get_item(Key={"WLSU_ID": wlsu_id})
        item = response.get('Item')
        if item is None:
            raise HTTPException(status_code=404, detail="WLSU not found")

        # Use `list_append` to add new data to `data_history`
        response = wlsus_table.update_item(
            Key={"WLSU_ID": wlsu_id},
            UpdateExpression="SET data_history = list_append(if_not_exists(data_history, :empty_list), :new_data)",
            ExpressionAttributeValues={
                ':new_data': [data_history],
                ':empty_list': []
            },
            ReturnValues="UPDATED_NEW"
        )

        return {"message": "Data updated"}

    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])    
@AwsAPIRouter.post("/areas/", response_model=Area)
async def create_area(area: Area):
    try:
        item = {
            'AREA_ID': area.AREA_ID,
            'AREA_NAME' : area.AREA_NAME,
            'L1N1': list(area.L1N1),
            'L2N2': list(area.L2N2),
            'status': bool(area.STATUS),
            'TImestamp': area.TIMESTAMP.isoformat(),
            'Zone_id': area.ZONE_ID
        }
        db = get_dynamodb_resource()
        wlsus_table = db.Table("area")
        result = wlsus_table.put_item(Item=item)
        return {"message": "Inserted Successfully"}

    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@AwsAPIRouter.post("/zones/", response_model=Zone)
async def create_zone(Zone: Zone):
    try:
        item = {
            'Zone-id': Zone.ZONE_ID,
            'city_id': Zone.CITY_ID,
            'L1N1': list(Zone.L1N1),
            'L2N2': list(Zone.L2N2),
            'STATUS': bool(Zone.STATUS),
            'TIMESTAMP': Zone.TIMESTAMP.isoformat(),
            'ZONE_NAME': Zone.ZONE_NAME
        }
        db = get_dynamodb_resource()
        wlsus_table = db.Table("Zone")
        result = wlsus_table.put_item(Item=item)
        return {"message": "Inserted Successfully"}

    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@AwsAPIRouter.post("/cedatives/", response_model=Cedative)
async def create_cedative(Cedative: Cedative):
    try:
        item = {
            'CEDATIVE_ID': Cedative.CEDATIVE_ID,
            'Backup_cedative_id' : Cedative.BACKUP_CEDATIVE_ID,
            'CLUSTER_ID': Cedative.CLUSTER_ID,
            'L1N2': list(Cedative.L1N2),
            'BL1N2': list(Cedative.BL1N2),
            'STATUS': bool(Cedative.STATUS),
            'TIMESTAMP': Cedative.TIMESTAMP.isoformat(),
            'wlsu_id': Cedative.WLSU_ID
        }
        db = get_dynamodb_resource()
        wlsus_table = db.Table("CEDATIVE")
        result = wlsus_table.put_item(Item=item)
        return {"message": "Inserted Successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@AwsAPIRouter.post("/clusters/", response_model=Cluster)
async def create_cluster(cluster: Cluster): 
    try:
        item = {
            'CLUASTER_ID': cluster.CLUASTER_ID,
            'AREA_ID': cluster.AREA_ID,
            'CEDATIVE_ID': cluster.CEDATIVE_ID,
            'CITY_ID': cluster.CITY_ID,
            'CLUSTER_NAME': cluster.CLUSTER_NAME,
            'L1N1': list(cluster.L1N1),
            'L2N2': list(cluster.L2N2),
            'STATUS': bool(cluster.STATUS),
            'TIMESTAMP': cluster.TIMESTAMP.isoformat(),
            'ZONE_ID': cluster.ZONE_ID
        }
        db = get_dynamodb_resource()
        wlsus_table = db.Table("CLUSTER")
        result = wlsus_table.put_item(Item=item)
        return {"message": "Inserted Successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@AwsAPIRouter.get("/wlsus/", response_model=List[WLSU])
async def get_wlsus():
    db = get_dynamodb_resource()
    wlsus_table = db.Table("WLSU")
    try:
        result = wlsus_table.scan()
        items = result.get('Items', [])
        return items
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message']) 
@AwsAPIRouter.get("/areas/", response_model=List[Area])
async def get_areas():
    db = get_dynamodb_resource()
    area_table = db.Table("area")
    try:
        result = area_table.scan()
        items = result.get('Items', [])
        while 'LastEvaluatedKey' in result:
            result = area_table.scan(ExclusiveStartKey=result['LastEvaluatedKey'])
            items.extend(result.get('Items', []))
        return items
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
#TODO: there is some unusal error
@AwsAPIRouter.get("/clusters/", response_model=List[Cluster])
async def get_clusters():
    db = get_dynamodb_resource()
    CLUSTER_table = db.Table("CLUSTER")
    try:
        result = CLUSTER_table.scan()
        items = result.get('Items', [])
        return items
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])

@AwsAPIRouter.get("/cedatives/", response_model=List[Cedative])
async def get_cedatives():
    """
    Retrieve a list of all cedative items from the CEDATIVE table in DynamoDB.

    Returns:
        List[Cedative]: A list of cedative items.

    Raises:
        HTTPException: Raises a 400 error if there's a client error while fetching items.
    """
    db = get_dynamodb_resource()
    CEDATIVE_table = db.Table("CEDATIVE")
    try:
        result = CEDATIVE_table.scan()
        items = result.get('Items', [])
        while 'LastEvaluatedKey' in result:
            result = CEDATIVE_table.scan(ExclusiveStartKey=result['LastEvaluatedKey'])
            items.extend(result.get('Items', []))
        return items
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
#TODO:there is some unusal error 
@AwsAPIRouter.get("/zones/", response_model=List[Zone])
async def get_zones():
    db = get_dynamodb_resource()
    Zone_table = db.Table("Zone")
    try:
        result = Zone_table.scan()
        items = result.get('Items', [])
        while 'LastEvaluatedKey' in result:
            result = Zone_table.scan(ExclusiveStartKey=result['LastEvaluatedKey'])
            items.extend(result.get('Items', []))
        return items
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
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
@AwsAPIRouter.get("/areas/{area_id}", response_model=Area)
async def get_area(area_id: str):
    db = get_dynamodb_resource()
    area_table = db.Table("area")
    try:
        response = area_table.get_item(Key={"AREA_ID":area_id})
        item = response.get('Item')
        if item is None:
            raise HTTPException(status_code=404, detail="area not found")
        return item
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
@AwsAPIRouter.get("/clusters/{cluster_id}", response_model=Cluster)
async def get_cluster(cluster_id: str):
    db = get_dynamodb_resource()
    CLUASTER_table = db.Table("CLUSTER")
    try:
        response = CLUASTER_table.get_item(Key={"CLUASTER_ID":cluster_id})
        item = response.get('Item')
        if item is None:
            raise HTTPException(status_code=404, detail="CLUSTER not found")
        return item
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
@AwsAPIRouter.get("/cedatives/{cedative_id}", response_model=Cedative)
async def get_cedative(cedative_id: str):
    db = get_dynamodb_resource()
    CEDATIVE_table = db.Table("CEDATIVE")
    try:
        response = CEDATIVE_table.get_item(Key={"CEDATIVE_ID":cedative_id})
        item = response.get('Item')
        if item is None:
            raise HTTPException(status_code=404, detail="CEDATIVE not found")
        return item
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
@AwsAPIRouter.get("/zones/{zone_id}")
async def get_zone(zone_id: str):
    db = get_dynamodb_resource()
    Zone_table = db.Table("Zone")
    try:
        response = Zone_table.get_item(Key={"Zone-id":zone_id})
        item = response.get('Item')
        if item is None:
            raise HTTPException(status_code=404, detail="Zone not found")
        return item
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
@AwsAPIRouter.delete("/wlsus/{wlsu_id}")
async def delete_wlsu(wlsu_id: str):
    db = get_dynamodb_resource()
    wlsus_table = db.Table("WLSU")
    try:
        response = wlsus_table.delete_item(Key={"WLSU_ID": wlsu_id})
        if response.get('HTTPStatusCode') != 200:
            raise HTTPException(status_code=404, detail="WLSU not found")
        return {"message": "WLSU deleted successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
@AwsAPIRouter.delete("/clusters/{cluster_id}")
async def delete_cluster(cluster_id: str):
    db = get_dynamodb_resource()
    CLUASTER_table = db.Table("CLUSTER")
    try:
        response = CLUASTER_table.delete_item(Key={"CLUASTER_ID": cluster_id})
        if response.get('Attributes') is None:
            raise HTTPException(status_code=404, detail="CLUASTER not found")
        return {"message": "CLUASTER deleted successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
@AwsAPIRouter.delete("/areas/{area_id}")
async def delete_area(area_id: str):
    db = get_dynamodb_resource()
    area_table = db.Table("area")
    try:
        response = area_table.delete_item(Key={"AREA_ID": area_id})
        if response.get('Attributes') is None:
            raise HTTPException(status_code=404, detail="Area not found")
        return {"message": "Area deleted successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
@AwsAPIRouter.delete("/cedatives/{cedative_id}")
async def delete_cedative(cedative_id: str):
    db = get_dynamodb_resource()
    CEDATIVE_table = db.Table("CEDATIVE")
    try:
        response = CEDATIVE_table.delete_item(Key={"CEDATIVE_ID": cedative_id})
        if response.get('Attributes') is None:
            raise HTTPException(status_code=404, detail="CEDATIVE not found")
        return {"message": "CEDATIVE deleted successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message'])
@AwsAPIRouter.delete("/zones/{zone_id}")
async def delete_zone(zone_id: str):
    db = get_dynamodb_resource()
    Zone_table = db.Table("Zone")
    try:
        response = Zone_table.delete_item(Key={"Zone-id": zone_id})
        if response.get('Attributes') is None:
            raise HTTPException(status_code=404, detail="Zone not found")
        return {"message": "Zone deleted successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.response['Error']['Message']) 
@AwsAPIRouter.get("/",response_class=JSONResponse)
async def add_zone(request:Request):
    return {"Hello":"World"}
@AwsAPIRouter.get("/RouteData")
async def find_route_data(route_data: dict = Body(...)):
    turning_points = [
        (str(point['latitude']), str(point['longitude'])) 
        for point in route_data['turning_points']
    ]
    wlsus_list = list(await get_wlsus())
    data = {}
    for i in range(len(turning_points) - 1):
        loc1 = turning_points[i]
        loc2 = turning_points[i + 1]        
        for wlsu in wlsus_list:
            wlsu_coordinates = tuple(wlsu.get("L1N1"))            
            if (loc1[0] <= wlsu_coordinates[0] <= loc2[0]) and (loc1[1] <= wlsu_coordinates[1] <= loc2[1]):
                key = f"{loc1}-{loc2}"
                data[key] = wlsu.get("data_history")[0]
    
    return jsonable_encoder(data)
