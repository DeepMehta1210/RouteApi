from fastapi import APIRouter
import models
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from config.db import connection
from fastapi.templating import Jinja2Templates

AwsAPIRouter=APIRouter()

@AwsAPIRouter.get("/",response_class=JSONResponse)
async def add_zone(request:Request):
    pass