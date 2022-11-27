import os
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from utils import extract_user, get_file_id, get_poster, last_online
import time
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Client.on_message(filters.command(["imdb", 'search']))
async def imdb_search(client, message):
    if ' ' in message.text:
        k = await message.reply('Searching ImDB')
        r, title = message.text.split(None, 1)
        movies = await get_poster(title, bulk=True)
        if not movies:
            return await message.reply("No results Found")
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('year')}",
                    callback_data=f"imdb#{movie.movieID}",
                )
            ]
            for movie in movies
        ]
        await k.edit('Here is what i found on IMDb', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('Give me a movie / series Name')

@Client.on_callback_query(filters.regex('^imdb'))
async def imdb_callback(bot: Client, query: CallbackQuery):
    i, movie = query.data.split('#')
    imdb = await get_poster(query=movie, id=True)
    btn = [
            [
                InlineKeyboardButton(
                    text=f"{imdb.get('title')} - {imdb.get('year')}",
                    url=imdb['url'],
                )
            ]
        ]
    if imdb.get('poster'):
        await query.message.reply_photo(photo=imdb['poster'], caption=f"<b>🎬 Title:</b> <a href={url}>{title}</a>\n<b>📆 Release:</b> <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>\n<b>🌟 Rating:</b> <a href={url}/ratings>{rating} / 10</a>\n(based on <code>{votes}</code> user ratings.)\n\n<b>🎭 Genres:</b> #{genres}\n<b>📀 Runtime:</b> <code>{runtime} minutes</code>\n\n<b>☀️ Languages:</b> #{languages}\n<b>🌎 Country of Origin:</b> #{countries}\n<b>🎥 Director:</b> {director}\n\n<b>✍️ Note:</b> This message will be Auto-deleted after 10 minutes to avoid copyright issues.", reply_markup=InlineKeyboardMarkup(btn))
        await query.message.delete()
    else:
        await query.message.edit(f"<b>🎬 Title:</b> <a href={url}>{title}</a>\n<b>📆 Release:</b> <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>\n<b>🌟 Rating:</b> <a href={url}/ratings>{rating} / 10</a>\n(based on <code>{votes}</code> user ratings.)\n\n<b>🎭 Genres:</b> #{genres}\n<b>📀 Runtime:</b> <code>{runtime} minutes</code>\n\n<b>☀️ Languages:</b> #{languages}\n<b>🌎 Country of Origin:</b> #{countries}\n<b>🎥 Director:</b> {director}\n\n<b>✍️ Note:</b> This message will be Auto-deleted after 10 minutes to avoid copyright issues.", reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
    await query.answer()
