import re
from os import environ
from ast import literal_eval as eval
id_pattern = re.compile(r'^.\d+$')


# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ.get('API_ID', '26248857'))
API_HASH = environ.get('API_HASH', '9ecc044d9b122a351b9d9b6b8ceaa1c4')
BOT_TOKEN = environ.get('BOT_TOKEN', '5578958108:AAHzJ0FbtwxbzheaH8xuL1XWhvzt_1-uePc')

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))
PICS = (environ.get('PICS', 'https://telegra.ph/file/857900020bd34fcba6fc2.jpg')).split()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '5630723610').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', "-1001817519178").split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel
AUTH_GROUPS = [int(admin) for admin in environ.get("AUTH_GROUPS", "").split()]

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://Bikash:Bikashji@cluster0.zugvr6j.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = environ.get('DATABASE_NAME', "Bikashji")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# Others
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1001617384911'))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', '')
P_TTTI_SHOW_OFF = eval((environ.get('P_TTTI_SHOW_OFF', "True")))
IMDB = eval((environ.get('IMDB', "False")))
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", None)

# IMDB template 
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>🎬 Title:</b> <a href={url}>{title}</a> [{year}] —<b>{kind}</b>\n\n<b>📆 Release:</b> <a href={url}/releaseinfo>{release_date}</a>\n<b>🌟 Rating:</b> <a href={url}/ratings>{rating} / 10</a>\n(based on <code>{votes}</code> user ratings.)\n\n<b>🎭 Genres:</b> #{genres}\n<b>📀 Runtime:</b> <code>{runtime} minutes</code>\n\n<b>☀️ Languages:</b> #{languages}\n<b>🌎 Country of Origin:</b> #{countries}\n<b>🎥 Director:</b> {director}\n\n<b>✍️ Note:</b>This message will be Auto-deleted after 20 minutes to avoid copyright issues.")
