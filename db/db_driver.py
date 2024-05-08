import motor.motor_asyncio
import os
import asyncio
from bson.objectid import ObjectId

MONGO_URI = os.environ.get("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
client.get_io_loop = asyncio.get_running_loop

database = client.thesis  # TODO: change this database
