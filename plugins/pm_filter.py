#Kanged From @Hello_Mr_Lucifer
import asyncio
import re
import ast
import datetime
import pytz
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, make_inactive
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTTI_SHOW_OFF, IMDB, IMDB_TEMPLATE
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums 
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, temp
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.filters_mdb import(
   del_all,
   find_filter,
   get_filters,
)

BUTTONS = {}

@Client.on_message(filters.command("alive"))
async def alive(client, message):
    await message.reply_text("I'm Not Dead...")

@Client.on_message(filters.command("link"))
async def link(client, message):
    await message.reply_text("♨️♨️ Are You Movie Lover ? ♨️\n\n🎬 Then You Are Welcomed To My Group For A Daily Breeze Of Movies\n༺━━━━━━━ ✧ ━━━━━━━༻\n\n📌 Old & New Movies/Series\n\n📌 Proper HD, DVD-Rip & Tv-Rip\n\n📌 Available In Various Size\n\n📌 Bengali | Hindi | English & More\n\n༺━━━━━━━ ✧ ━━━━━━━༻\n\n✔️ Group - https://t.me/+t3qvm0BMklkyZGIx\n\n👆Click Link For Join Group")

@Client.on_message(filters.group & filters.text & filters.chat(-1001768250325) & filters.incoming)
async def give_filter(client,message):
    group_id = message.chat.id
    name = message.text

    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await message.reply_text(reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await message.reply_text(
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button)
                            )
                    elif btn == "[]":
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or ""
                        )
                    else:
                        button = eval(btn) 
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button)
                        )
                except Exception as e:
                    print(e)
                break 

    else:
        await auto_filter(client, message)   

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):

    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("oKda", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    btn = [
        [
            InlineKeyboardButton(
                text=f"{file.file_name}", callback_data=f'files#{file.file_id}'
            ),
            InlineKeyboardButton(
                text=f"| {get_size(file.file_size)} |",
                callback_data=f'files_#{file.file_id}',
            ),
        ]
        for file in files
    ]

    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("🔙 Back", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"📃 Pages {round(int(offset)/10)+1} / {round(total/10)}", callback_data="pages"), InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"https://t.me/{temp.U_NAME}")]
                )    
        btn.append(
            [InlineKeyboardButton(f"🗓 {round(int(offset) / 10) + 1} / {round(total / 10)}", callback_data="pages"),
             InlineKeyboardButton("🗑️", callback_data="close"),
             InlineKeyboardButton("⚠️ Faq", callback_data="faq")]
        )
        btn.append(
                [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"https://t.me/{temp.U_NAME}")]
        )
    else:
        btn.append(
            [
                InlineKeyboardButton("🔙 Back Page", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"🗓 {round(int(offset) / 10) + 1} / {round(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("Next Page ➡", callback_data=f"next_{req}_{key}_{n_offset}")]
            )
    btn.insert(0, [
        InlineKeyboardButton(text="ミ★ MOVIE TIME ★彡", callback_data="rsrq"),
    ])
    btn.insert(0, [
        InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"https://t.me/{temp.U_NAME}")
    ])
    try:
        await query.edit_message_reply_markup( 
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()

    
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            grpid  = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == "creator") or (str(userid) in ADMINS):    
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!",show_alert=True)

    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == "creator") or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Thats not for you!!",show_alert=True)


    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]
        title = query.data.split(":")[2]
        act = query.data.split(":")[3]
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}:{title}"),
                InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode="md"
        )
        return

    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]
        title = query.data.split(":")[2]
        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text('Some error occured!!', parse_mode="md")
        return
    elif "disconnect" in query.data:
        await query.answer()

        title = query.data.split(":")[2]
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text('Some error occured!!', parse_mode="md")
        return
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text('Some error occured!!', parse_mode="md")
        return
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{title}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert,show_alert=True)

    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        files = (await get_file_details(file_id))[0]
        title = files.file_name
        size=get_size(files.file_size)
        f_caption=files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
            except Exception as e:
                print(e)
            f_caption=f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"
        buttons = [[
               InlineKeyboardButton('🆘👤 Owner', url='https://t.me/Hello_Professor_99'),
               InlineKeyboardButton('🆘🤖 Contact', url='https://t.me/Hello_Professor_99')
               ],[
               InlineKeyboardButton(text="⁉️ Want To Save/Share This File", callback_data="scst")
               ],[
               InlineKeyboardButton('🗑 Close File', callback_data='close')]]
        try:  
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={file_id}")
                return
            elif P_TTTI_SHOW_OFF:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={file_id}")
                return
            else:
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption
                    )
                await query.answer('Check Bot PM, I Have Sent Your Files In PM 📩',show_alert = True)
        except UserIsBlocked:
            await query.answer('Unblock the bot mahn !',show_alert = True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={file_id}")

    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files = (await get_file_details(file_id))[0]
        title = files.file_name
        size=get_size(files.file_size)
        f_caption=files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
            except Exception as e:
                print(e)
                f_caption=f_caption
        if f_caption is None:
            f_caption = f"{title}"
        buttons = [[
               InlineKeyboardButton('🆘👤 Owner', url='https://t.me/Hello_Professor_99'),
               InlineKeyboardButton('🆘🤖 Contact', url='https://t.me/Hello_Professor_99')
               ],[
               InlineKeyboardButton(text="⁉️ Want To Save/Share This File", callback_data="scst")
               ],[
               InlineKeyboardButton('🗑 Close File', callback_data='close')]]
    elif "scst" in query.data:
        return await query.answer("""
» HERE IS THE SOLUTION «

☞ Send Me Rs.50/- Per Month With Payment Proof

UPI 🆔 Details

Gpay 📲 joynathnet4@oksbi
Phonepe 📲 Soon...

✔️ After Payment Verification Your ID Well Be Freed
""", show_alert=True)
        await query.answer()
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            protect_content=True if ident == 'checksubp' else False
        )
    elif query.data == "pages":
        await query.answer()
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('➕ Click Here For More Buttons ➕', callback_data='professor_99')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        now=datetime.datetime.now()
        tz=pytz.timezone('Asia/Kolkata')
        yn=now.astimezone(tz)
        hour=yn.hour
        if hour < 12:
          greeting="Good Morning"
        elif hour < 15:
          greeting="Good Afternoon"
        elif hour < 20:
          greeting="Good Evening"
        else:
          greeting="Good Night"
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, greeting),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "professor_99":
        buttons = [[
            InlineKeyboardButton('🔗 Movie Time', url='https://t.me/+t3qvm0BMklkyZGIx'),
            ],[
            InlineKeyboardButton('ℹ️ Help', callback_data='help'),
            InlineKeyboardButton(text='😎 About', callback_data='about')
            ],[
            InlineKeyboardButton('🔙 Back', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="▣ ▢ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▣"
        )       
        await query.message.edit_text(
            text=script.ALIVE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await query.message.edit_text(
            text=script.PROFESSOR_99.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('🚨 Alive', callback_data='alive'),
            InlineKeyboardButton('🔍 IMDB', callback_data='imdb'),
            InlineKeyboardButton('🔗 Link', callback_data='link')
            ],[
            InlineKeyboardButton('⚠️ Faq', callback_data='faq'),
            InlineKeyboardButton('🆔 Ids', callback_data='ids'),
            InlineKeyboardButton('🎼 Song', callback_data='song')
            ],[
            InlineKeyboardButton('😎 About', callback_data='about'),
            InlineKeyboardButton('🏠 Home', callback_data='professor_99'),
            InlineKeyboardButton('❎ Close', callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="▣ ▢ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▣"
        )       
        await query.message.edit_text(
            text=script.ALIVE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif "about" in query.data:
        return await query.answer("""
꧁֍MOVIE TIME BOT֍꧂

🤴 Creator: MR.Lucifer
❖ Language: Python3
❖ Hosted: Heroku 
❖ Version: 2.0.1 [BETA]
❖ Farmework: Pyrogram
❖ Database: MongoDB
֎ Bot: Indian 🇮🇳
""", show_alert=True)
    
    elif "rsrq" in query.data:
        return await query.answer("""
ミ★ MOVIE TIME ★彡

☞ Sᴛᴏʀᴀɢᴇ Oғ Nᴇᴡ & Oʟᴅ Mᴏᴠɪᴇs/Sᴇʀɪᴇs
☞ Aᴠᴀɪʟᴀʙʟᴇ Iɴ Mᴀɴʏ Sɪᴢᴇs & Lᴀɴɢᴜᴀɢᴇs
☞ Rᴇᴄᴇɪᴠᴀʙʟᴇ Iɴ Vᴀʀɪᴏᴜs Qᴜᴀʟɪᴛʏ

👑
MR.Lucifer 
""", show_alert=True)

    elif query.data == "alive":
        buttons = [[
            InlineKeyboardButton('🔙 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="▣ ▢ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▣"
        )       
        await query.message.edit_text(
            text=script.ALIVE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "imdb":
        buttons = [[
            InlineKeyboardButton('🔙 Back', callback_data='help'),
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="▣ ▢ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▣"
        )       
        await query.message.edit_text(
            text=script.IMDB_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "link":
        buttons = [[
            InlineKeyboardButton('🔙 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="▣ ▢ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▣"
        )       
        await query.message.edit_text(
            text=script.LINK_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "faq":
        buttons = [[
            InlineKeyboardButton('বাংলা', callback_data='bengali'),
            InlineKeyboardButton('हिंदी', callback_data='hindi'),
            ],[
            InlineKeyboardButton('English', callback_data='english'),
            ],[
            InlineKeyboardButton('🔙 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="▣ ▢ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▣"
        )       
        await query.message.edit_text(
            text=script.FAQ_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "ids":
        buttons = [[
            InlineKeyboardButton('🔙 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="▣ ▢ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▣"
        )       
        await query.message.edit_text(
            text=script.IDS_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "song":
        buttons = [[
            InlineKeyboardButton('🔙 Back', callback_data='help'),  
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="▣ ▢ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▢"
        )
        await query.message.edit_text(
            text="▣ ▣ ▣"
        )       
        await query.message.edit_text(
            text=script.SONG_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
async def auto_filter(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:
        
        search = message.text
        files, offset, total_results = await get_search_results(search.lower(), offset=0)
        if not files:
            return
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}",
                    callback_data=f'files#{file.file_id}',
                ),
                InlineKeyboardButton(
                    text=f"| {get_size(file.file_size)} |",
                    callback_data=f'files_#{file.file_id}',
                ),
            ]
            for file in files
        ]

        if offset != "":
            key = f"{message.chat.id}-{message.message_id}"
            BUTTONS[key] = search
            req = message.from_user.id if message.from_user else 0
            btn.append(
                [InlineKeyboardButton(text="Next Page ➡", callback_data=f"next_{req}_{key}_{offset}")]
            )    
            btn.append(
                [InlineKeyboardButton(text=f"🗓 1/{round(int(total_results) / 10)}", callback_data="pages"),
                 InlineKeyboardButton("🗑️", callback_data="close"),
                 InlineKeyboardButton("⚠️ Faq", callback_data="faq")]
            )
            btn.append(
                [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"https://t.me/{temp.U_NAME}")]
            )
        else:
            btn.append(
                [InlineKeyboardButton(text="🗓 1/1", callback_data="pages"),
                 InlineKeyboardButton("🗑️", callback_data="close"),
                 InlineKeyboardButton("⚠️ Faq", callback_data="faq")]
            )
            btn.append(
                [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"https://t.me/{temp.U_NAME}")]
            )
        btn.insert(0, [
            InlineKeyboardButton(text="ミ★ MOVIE TIME ★彡", callback_data="rsrq"),
        ]) 
        imdb = await get_poster(search) if IMDB else None
    if imdb:
        cap = IMDB_TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        cap = f"<b>🎬 Title:</b> {search}\n</b>\n<b><a href='https://t.me/+q9NMdy0rY10zZWZl'>© IMDb (Series & Movies) Studio</a></b>\n\n<b>✍️ Note:</b> <s>This message will be Auto-deleted after 10 hours to avoid copyright issues.</s>"
    if imdb and imdb.get('poster'):
        try:
            hehe = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_to_message_id=reply_id, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(36000)
            await hehe.delete()
            await message.delete()
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            hmm = await message.reply_photo(photo=poster, caption=cap[:1024], reply_to_message_id=reply_id, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(36000)
            await hmm.delete()
            await message.delete()
        except Exception as e:
            logger.exception(e)
            fek = await message.reply_photo(photo="https://telegra.ph/file/82b5bbbab6d5e5593b6b2.jpg", caption=cap, reply_to_message_id=reply_id, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(36000)
            await fek.delete()
            await msg.delete()
    else:
        fuk = await message.reply_photo(photo="https://telegra.ph/file/8b42f6caf6ef5fd76766f.jpg", caption=cap, reply_to_message_id=reply_id, reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(36000)
        await fuk.delete()
        await msg.delete()
    if spoll:
        await msg.message.delete()

