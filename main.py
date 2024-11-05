from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.GujcostRoute import AwsAPIRouter
from mangum import Mangum
app = FastAPI()
app.include_router(AwsAPIRouter)
handler=Mangum(app=app,)
# app.mount("/static",StaticFiles(directory="static"),name="static")
# templates=Jinja2Templates(directory="templates")