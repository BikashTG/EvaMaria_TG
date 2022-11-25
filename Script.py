class script(object):
    START_TXT = """<i><b>Hello 👋 {},</i></b>

<i><b>I Am Not Only <a href="https://t.me/LuciferMorningStar_Robot">Lucifer Moringstar Robot</a> To Assist You But Also Employed At <a href="https://t.me/+t3qvm0BMklkyZGIx">Movie Time</a> Group By <a href="https://t.me/Hello_Professor_99">PROFESSOR-99</a> So You Can't Get My Service By Adding Me To Your Group So Don't Waste Your Time & Data</i></b> 😉

<i><b>Better You Click Below & Join <a href="https://t.me/+t3qvm0BMklkyZGIx">Movie Time</a> & Feel The Experience Of Downloading Unlimited Movies/Series</i></b> ✅

<i><b>For More Information Click ℹ️ Help</i></b>"""
     
    HELP_TXT = """<i><b>Hello 👋 {},</i></b>

<i><b>I can Guide You Through All Of <a href="https://t.me/LuciferMorningStar_Robot">Lucifer Moringstar Robot</a>'s Cool Features & How To Properly Use Them. Use The Buttons Below To Navigate Through All Of The Modules.</i></b>"""

    PROFESSOR_99 = """<i><b>Hello 👋 {},</i></b>

<i><b>I Am Not Only <a href="https://t.me/LuciferMorningStar_Robot">Lucifer Moringstar Robot</a> To Assist You But Also Employed At <a href="https://t.me/+t3qvm0BMklkyZGIx">Movie Time</a> Group By <a href="https://t.me/hellodarklord">PROFESSOR-99</a> So You Can't Get My Service By Adding Me To Your Group So Don't Waste Your Time & Data</i></b> 😉

<i><b>Better You Click Below & Join <a href="https://t.me/+t3qvm0BMklkyZGIx">Movie Time</a> & Feel The Experience Of Downloading Unlimited Movies/Series</i></b> ✅

<i><b>For More Information Click ℹ️ Help</i></b>"""
     
    
    MANUELFILTER_TXT = """Help: <b>Filters</b>

- Filter is the feature were users can set automated replies for a particular keyword and tessa will respond whenever a keyword is found the message

<b>Commands and Usage:</b>
• /filter - <code>add a filter in chat</code>
• /filters - <code>list all the filters of a chat</code>
• /del - <code>delete a specific filter in chat</code>
• /delall - <code>delete the whole filters in a chat (chat owner only)</code>"""

    BUTTON_TXT = """Help: <b>Buttons</b>

- Lucifer Bot Supports both url and alert inline buttons.

<b>URL buttons:</b>
<code>[Button Text](buttonurl:https://t.me/IMDB_HPBot)</code>

<b>Alert buttons:</b>
<code>[Button Text](buttonalert:This is an alert message)</code>"""

    AUTOFILTER_TXT = """Help: <b>Auto Filter</b>

<b>NOTE:</b>
1. Make me the admin of your channel if it's private.
2. make sure that your channel does not contains camrips, porn and fake files.
3. Forward the last message to me with quotes.
 I'll add all the files in that channel to my db."""

    CONNECTION_TXT = """Help: <b>Connections</b>

- Used to connect bot to PM for managing filters 
- it helps to avoid spamming in groups.

<b>Commands and Usage:</b>
• /connect  - <code>connect a particular chat to your PM</code>
• /disconnect  - <code>disconnect from a chat</code>
• /connections - <code>list all your connections</code>"""

    EXTRAMOD_TXT = """Help: <b>Extra Modules</b>

<b>NOTE:</b>
these are the extra features of tessa

<b>Commands and Usage:</b>
• /id - <code>get id of a specifed user.</code>
• /info  - <code>get information about a user.</code>
• /imdb  - <code>get the film information from IMDb source.</code>
• /search  - <code>get the film information from various sources.</code>"""
    ADMIN_TXT = """Help: <b>Admin mods</b>

<b>NOTE:</b>
This module only works for my admins

<b>Commands and Usage:</b>
• /logs - <code>to get the rescent errors</code>
• /stats - <code>to get status of files in db.</code>
• /users - <code>to get list of my users and ids.</code>
• /chats - <code>to get list of the my chats and ids </code>
• /leave  - <code>to leave from a chat.</code>
• /disable  -  <code>do disable a chat.</code>
• /ban  - <code>to ban a user.</code>
• /unban  - <code>to unban a user.</code>
• /channel - <code>to get list of total connected channels</code>
• /broadcast - <code>to broadcast a message to all users</code>"""

    STATUS_TXT = """★ 𝚃𝙾𝚃𝙰𝙻 𝙵𝙸𝙻𝙴𝚂: <code>{}</code>
★ 𝚃𝙾𝚃𝙰𝙻 𝚄𝚂𝙴𝚁𝚂: <code>{}</code>
★ 𝚃𝙾𝚃𝙰𝙻 𝙲𝙷𝙰𝚃𝚂: <code>{}</code>
★ 𝚄𝚂𝙴𝙳 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝚒𝙱
★ 𝙵𝚁𝙴𝙴 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝚒𝙱"""

    LOG_TEXT_G = """#NewGroup
Group = {}(<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}
"""
    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Name - {}
"""
