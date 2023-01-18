import asyncio,logging,os,re,shutil
from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
load_dotenv(override=True)

API_ID = os.getenv('TG_API_ID')
API_HASH = os.getenv('TG_API_HASH')

def get_session_files():
    all_files = os.listdir('files')
    for file in all_files:
        if re.match('^\d+\.txt$', file):
            with open('files/{}'.format(file), 'r') as f:
                fdata = f.read()
                yield [line.strip().split(': ')[1] for line in fdata.split('\n')]
async def main():
    for session in get_session_files():
        try:
            client = TelegramClient(StringSession(session[2]), API_ID, API_HASH)
            await client.connect()
            authorized = await client.is_user_authorized()
            await client.disconnect()
        except Exception as e:
            print(repr(e))
            authorized = False
        if authorized:
            shutil.copy('files/{}.txt'.format(session[0][1:]), 'active/{}.txt'.format(session[0][1:]))
            print('user is authorized')
        else:
            print('user is NOT authorized')

if not os.path.isdir('files'):
    print('files directory not found !')
    exit()
if not os.path.isdir('active'):
    os.makedirs('active')
asyncio.run(main())