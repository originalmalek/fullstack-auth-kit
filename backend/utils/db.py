from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

# Global variables for database connection
client: AsyncIOMotorClient = None
db = None
users_collection = None

def init_database():
    '''Initialize database connection'''
    global client, db, users_collection
    
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    users_collection = db['users']


def get_users_collection():
    '''Get users collection'''
    return users_collection


def get_database():
    '''Get database instance'''
    return db


async def get_user_by_username(username: str):
    '''Get user by username'''
    return await users_collection.find_one({'username': username})


async def get_user_by_id(user_id: str):
    '''Get user by ID'''
    from bson import ObjectId
    try:
        return await users_collection.find_one({'_id': ObjectId(user_id)})
    except Exception:
        return None


async def connect_to_mongo():
    '''Connect to MongoDB on application startup'''
    init_database()
    # Test the connection
    try:
        await client.admin.command('ping')
        print('✅ Successfully connected to MongoDB')
    except Exception as e:
        print(f'❌ Error connecting to MongoDB: {e}')

async def close_mongo_connection():
    '''Close MongoDB connection on application shutdown'''
    if client:
        client.close()
        print('✅ MongoDB connection closed')
