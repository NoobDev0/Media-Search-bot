#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from pyrogram.errors import UserNotParticipant
from .translation import Text
from utils import get_filter_results, get_file_details, is_subscribed, get_details
BUTTONS = {}
BOT = {}
@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAACAgUAAxkBAAEDGFZhasSMEft-_11k3ofgSwtMqAMjpwACIQMAAkwLaVcGrn3X7HM5cCEE')
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📑 𝖯𝖺𝗀𝖾𝗌 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                dict=await get_details(search)
                poster=dict["image"] 
                titlee=dict["title"]
                yearr=dict["year"]
                ratingg=dict["rating"]
                genree=dict["genre"]
                ratedd=dict["rated"]
            if poster:
                await message.reply_photo(photo=poster, caption=f"🎬 <b>Movie/Series</b> : <code>{titlee}</code> /n🔥 <b>Released</b> : <code>{yearr}</code> /n💫 <b>Rating</b> : <code>{ratingg}</code> /n🎭 <b>Genre</b> : <code>{genree}</code> /n✔ <b>Rated</b> : <code>{ratedd}</code> /n <u>@Cinema_Haunter</u>", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="📥 𝖭𝖾𝗑𝗍",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📑 𝖯𝖺𝗀𝖾𝗌 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            dict=await get_details(search)
            poster=dict["image"]
            titlee=dict["title"]
            yearr=dict["year"]
            ratingg=dict["rating"]
            genree=dict["genre"]
            ratedd=dict["rated"]
        if poster:
            await message.reply_photo(photo=poster, caption=f"🎬 <b>Movie/Series</b> : <code>{titlee}</code> /n🔥 <b>Released</b> : <code>{yearr}</code> /n💫 <b>Rating</b> : <code>{ratingg}</code> /n🎭 <b>Genre</b> : <code>{genree}</code> /n✔ <b>Rated</b> : <code>{ratedd}</code> /n <u>@Cinema_Haunter</u>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}")]
                )
        else:
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📑 𝖯𝖺𝗀𝖾𝗌 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                dict=await get_details(search)
                poster=dict["image"]
                titlee=dict["title"]
                yearr=dict["year"]
                ratingg=dict["rating"]
                genree=dict["genre"]
                ratedd=dict["rated"]
            if poster:
                await message.reply_photo(photo=poster, caption=f"🎬 <b>Movie/Series</b> : <code>{titlee}</code> /n🔥 <b>Released</b> : <code>{yearr}</code> /n💫 <b>Rating</b> : <code>{ratingg}</code> /n🎭 <b>Genre</b> : <code>{genree}</code> /n✔ <b>Rated</b> : <code>{ratedd}</code> /n <u>@Cinema_Haunter</u>", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(f"🎬 <b>Movie/Series</b> : <code>{titlee}</code> /n🔥 <b>Released</b> : <code>{yearr}</code> /n💫 <b>Rating</b> : <code>{ratingg}</code> /n🎭 <b>Genre</b> : <code>{genree}</code> /n✔ <b>Rated</b> : <code>{ratedd}</code> /n <u>@Cinema_Haunter</u>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="📥 𝖭𝖾𝗑𝗍",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📑 𝖯𝖺𝗀𝖾𝗌 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            dict=await get_details(search)
            poster=dict["image"] 
            titlee=dict["title"]
            yearr=dict["year"]
            ratingg=dict["rating"]
            genree=dict["genre"]
            ratedd=dict["rated"]
        if poster:
            await message.reply_photo(photo=poster, caption=f"🎬 <b>Movie/Series</b> : <code>{titlee}</code> /n🔥 <b>Released</b> : <code>{yearr}</code> /n💫 <b>Rating</b> : <code>{ratingg}</code> /n🎭 <b>Genre</b> : <code>{genree}</code> /n✔ <b>Rated</b> : <code>{ratedd}</code> /n <u>@Cinema_Haunter</u>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["𝖲𝗎𝖻𝗍𝗂𝗍𝗅𝖾", "𝖲𝗎𝖻𝗍𝗂𝗍𝗅𝖾", "𝖬𝖻", "𝖦𝖻", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("📤 𝖡𝖺𝖼𝗄", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📑 𝖯𝖺𝗀𝖾𝗌 {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("📤 𝖡𝖺𝖼𝗄", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📑 𝖯𝖺𝗀𝖾𝗌 {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("📥 𝖭𝖾𝗑𝗍 ", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📑 𝖯𝖺𝗀𝖾𝗌 {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("📤 𝖡𝖺𝖼𝗄", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📑 𝖯𝖺𝗀𝖾𝗌 {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "start":
            buttons = [[
                InlineKeyboardButton("📬 ℂ𝕙𝕒𝕟𝕟𝕖𝕝", url="https://t.me/CinemaHaunter"),
                InlineKeyboardButton("📧 𝔾𝕣𝕠𝕦𝕡", url="https://t.me/Cinema_Haunter")
            ],
            [
                InlineKeyboardButton("🎛 𝔽𝕖𝕒𝕥𝕦𝕣𝕖𝕤", callback_data="features"),
                InlineKeyboardButton("🎬 𝕊𝕖𝕒𝕣𝕔𝕙 𝕄𝕠𝕧𝕚𝕖𝕤", switch_inline_query_current_chat='') 
            ],
            [
                InlineKeyboardButton("📝 𝔸𝕓𝕠𝕦𝕥", callback_data="about")
            ]]
            
            await update.message.edit_text(
                TEXT.START_TEXT.format(update.from_user.mention),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode="html",
                disable_web_page_preview=True
            )
                

        elif query.data == "about":
            buttons = [[
                InlineKeyboardButton('𝕄𝕠𝕧𝕚𝕖 𝕌𝕡𝕕𝕒𝕥𝕖𝕤', url='https://t.me/movieupdates3000')
            ],
            [
                InlineKeyboardButton('𝔹𝕒𝕔𝕜', callback_data="features"),
                InlineKeyboardButton('ℂ𝕝𝕠𝕤𝕖', callback_data="close")
            ]]
            
            await query.message.edit(text="<b>Developer : <a href='https://t.me/M_VineshKumar'>Jonas</a>\nLanguage : <code>Python3</code>\nLibrary : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio</a>\nSource Code : <a href='https://github.com/subinps/Media-Search-bot'>Click here</a>\nUpdate Channel : <a href='https://t.me/CinemaHaunter'>Cinema Haunter</a>\nServer : <a href='https://heroku.com'>Heroku</a></b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
        
        elif query.data == "close":
            await update.message.delete()

        elif query.data == "features":
            buttons = [[
                InlineKeyboardButton('𝔸𝕦𝕥𝕠 𝔽𝕚𝕝𝕥𝕖𝕣', callback_data="auto"),
                InlineKeyboardButton('ℙ𝕞 𝔽𝕚𝕝𝕥𝕖𝕣', callback_data="filter")
            ],
            [
                InlineKeyboardButton('𝕀𝕟𝕝𝕚𝕟𝕖 𝕊𝕖𝕒𝕣𝕔𝕙', callback_data="search"),
                InlineKeyboardButton('𝕀𝕄𝔻𝕓 𝕀𝕟𝕗𝕠', callback_data="info")
            ],
            [
                InlineKeyboardButton('𝔹𝕒𝕔𝕜', callback_data="start")
            ]]

            await update.message.edit_text(
                Text.FEATURES.TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode="html",
                disable_web_page_preview=True
            )


        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
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
                buttons = [
                    [
                        InlineKeyboardButton('𝔸𝕕𝕞𝕚𝕟', url='https://t.me/M_VineshKumar'),
                        InlineKeyboardButton('𝕆𝕗𝕗𝕚𝕔𝕚𝕒𝕝 ℂ𝕙𝕒𝕟𝕟𝕖𝕝', url='https://t.me/CinemaHaunter)
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
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
                buttons = [
                    [
                        InlineKeyboardButton('𝔸𝕕𝕞𝕚𝕟', url='https://t.me/M_VineshKumar'),
                        InlineKeyboardButton('𝕆𝕗𝕗𝕚𝕔𝕚𝕒𝕝 ℂ𝕙𝕒𝕟𝕟𝕖𝕝', url='https://t.me/CinemaHaunter')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("👀",show_alert=True)
