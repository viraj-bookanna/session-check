import asyncio,logging,os,re,shutil
from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
load_dotenv(override=True)
mongo_client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))

def session_generator():
    database = mongo_client.userdb.sessions
    for session in database.find({'logged_in': True}):
        yield session['session']
async def main():
    for session in session_generator():
        try:
            client = TelegramClient(StringSession(session), os.getenv('API_ID'), os.getenv('API_HASH'))
            await client.connect()
            authorized = await client.is_user_authorized()
            me = await client.get_me()
            await client.disconnect()
        except Exception as e:
            print(repr(e))
            authorized = False
        if authorized:
            with open(f'active/+{me.phone}', 'w') as f:
                f.write(f'Phone: +{me.phone}\nSession: {session}\n')
            print('user is authorized')
        else:
            print('user is NOT authorized')

if not os.path.isdir('active'):
    os.makedirs('active')
asyncio.run(main())