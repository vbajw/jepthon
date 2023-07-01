from HuRe import l313l
from datetime import datetime
import time
from telethon.errors import FloodWaitError
import asyncio
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import AUTONAME, edit_delete, l313l, logging
normzltext = "1234567890"
namerzfont = Config.JP_FN or "𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢"
autoname_task = None

async def autonameS_loop():
    global autoname_task
    AUTONAMESTART = gvarstatus("autonameS") == "true"
    while AUTONAMESTART:
        current_time = datetime.now().strftime("%H:%M:%S")
        for normal in current_time:
            if normal in normzltext:
                namefont = namerzfont[normzltext.index(normal)]
                current_time = current_time.replace(normal, namefont)
        name = f"{lMl10l} {current_time}"
        LOGS.info(name)
        try:
            await l313l(functions.account.UpdateProfileRequest(last_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(1)
        time.sleep(1)  # استخدم time.sleep(1) بدلاً من asyncio.sleep(1)
        AUTONAMESTART = gvarstatus("autonameS") == "true"

@l313l.on(admin_cmd(pattern=f"اسم ثواني(?:\s|$)([\s\S]*)"))
async def _(event):
    if gvarstatus("autonameS") is not None and gvarstatus("autonameS") == "true":
        return await edit_delete(event, "**الاسـم الـوقتي شغـال بالأصـل 🧸♥**")
    addgvar("autonameS", True)
    await edit_delete(event, "**تم تفـعيل اسـم الـوقتي بنجـاح ✓**")
    if autoname_task is None:
        autoname_task = asyncio.create_task(autonameS_loop())

@l313l.on(admin_cmd(pattern="ايقاف ثواني$"))
async def _(event):
    if gvarstatus("autonameS") is not None and gvarstatus("autonameS") == "true":
        delgvar("autonameS")
        if autoname_task is not None:
            autoname_task.cancel()
            autoname_task = None
        await edit_delete(event, "**تم تعطيل اسـم الـوقتي بنجـاح ✓**")
    else:
        await edit_delete(event, "**اسـم الـوقتي معطـل بـالأصـل ❗**")