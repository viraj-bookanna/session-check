import logging,os,struct,base64,asyncio,re
from telethon.sessions.string import StringSession
from telethon.sync import TelegramClient
from dotenv import load_dotenv

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
load_dotenv(override=True)

API_ID = os.getenv('TG_API_ID')
API_HASH = os.getenv('TG_API_HASH')
    
def get_session_files():
    all_files = os.listdir('active')
    for file in all_files:
        if re.match('^\d+\.txt$', file):
            with open('active/{}'.format(file), 'r') as f:
                fdata = f.read()
                yield [line.strip().split(': ')[1] for line in fdata.split('\n')]
async def t2p(session):
    str_sess = StringSession(session[2])
    async with TelegramClient(str_sess, API_ID, API_HASH) as tclient:
        me = await tclient.get_me()
    return base64.urlsafe_b64encode(
        struct.pack(
            '>B?256sQ?',
            str_sess.dc_id,
            None,
            str_sess.auth_key.key,
            me.id,
            me.bot
        )).decode().rstrip("=")
async def main():
    j = ['Phone', 'Password', 'Session-string']
    for session in get_session_files():
        client = TelegramClient(StringSession(session[2]), API_ID, API_HASH)
        await client.connect()
        authorized = await client.is_user_authorized()
        await client.disconnect()
        if authorized:
            session[2] = await t2p(session)
            with open('pyrofiles/{}.txt'.format(session[0][1:]), 'w') as f:
                f.write('\n'.join([': '.join([j[i], session[i]]) for i in range(len(session))]))

if not os.path.isdir('active'):
    print('active directory not found !')
    exit()
if not os.path.isdir('pyrofiles'):
    os.makedirs('pyrofiles')
asyncio.run(main())