#    This file is part of the Compressor distribution.
#    Copyright (c) 2021 Danish_00
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in
# <https://github.com/1Danish-00/CompressorQueue/blob/main/License> .


from pyrogram import filters

from . import *
from .devtools import *

LOGS.info("Starting...")


######## Connect ########


try:
    bot.start(bot_token=BOT_TOKEN)
    app.start()
except Exception as er:
    LOGS.info(er)


####### GENERAL CMDS ########


@bot.on(events.NewMessage(pattern="/start"))
async def _(e):
    await start(e)


@bot.on(events.NewMessage(pattern="/ping"))
async def _(e):
    await up(e)


@bot.on(events.NewMessage(pattern="/help"))
async def _(e):
    await help(e)


@bot.on(events.NewMessage(pattern="/restart"))
async def _(e):
    await restart(e)


@bot.on(events.NewMessage(pattern="/nuke"))
async def _(e):
    await nuke(e)


@bot.on(events.NewMessage(pattern="/cancelall"))
async def _(e):
    await clean(e)


@bot.on(events.NewMessage(pattern="/showthumb"))
async def _(e):
    await getthumb(e)


@bot.on(events.NewMessage(pattern="/clear"))
async def _(e):
    await clearqueue(e)


######## Callbacks #########


@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"stats(.*)")))
async def _(e):
    await stats(e)


@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pres(.*)")))
async def _(e):
    await pres(e)


@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"skip(.*)")))
async def _(e):
    await skip(e)


@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"dl_stat(.*)")))
async def _(e):
    await dl_stat(e)


@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"cancel_dl(.*)")))
async def _(e):
    await cancel_dl(e)


@bot.on(events.callbackquery.CallbackQuery(data=re.compile("ihelp")))
async def _(e):
    await ihelp(e)


@bot.on(events.callbackquery.CallbackQuery(data=re.compile("beck")))
async def _(e):
    await beck(e)


########## Direct ###########


@bot.on(events.NewMessage(pattern="/eval"))
async def _(e):
    await eval(e)


@app.on_message(filters.incoming & filters.command(["peval"]))
async def _(app, message):
    await eval_message_p(app, message)


@app.on_message(filters.incoming & filters.command(["update"]))
async def _(app, message):
    await update2(app, message)


@bot.on(events.NewMessage(pattern="/bash"))
async def _(e):
    await bash(e)


@bot.on(events.NewMessage(pattern="/status"))
async def _(e):
    await status(e)


@bot.on(events.NewMessage(pattern="/parse"))
async def _(e):
    await discap(e)


@bot.on(events.NewMessage(pattern="/fix"))
async def _(e):
    await version2(e)


@bot.on(events.NewMessage(pattern="/filter"))
async def _(e):
    await filter(e)


@bot.on(events.NewMessage(pattern="/vfilter"))
async def _(e):
    await vfilter(e)


@bot.on(events.NewMessage(pattern="/delfilter"))
async def _(e):
    await rmfilter(e)


@bot.on(events.NewMessage(pattern="/reset"))
async def _(e):
    await reffmpeg(e)


@bot.on(events.NewMessage(pattern="/get"))
async def _(e):
    await check(e)


@bot.on(events.NewMessage(pattern="/set"))
async def _(e):
    await change(e)


@bot.on(events.NewMessage(pattern="/queue"))
async def _(e):
    await listqueue(e)


@bot.on(events.NewMessage(pattern="/lock"))
async def _(e):
    await lock(e)


@bot.on(events.NewMessage(pattern="/encodequeue"))
async def _(e):
    await listqueuep(e)


@bot.on(events.NewMessage(pattern="/groupenc"))
async def _(e):
    await allowgroupenc(e)


@bot.on(events.NewMessage(pattern="/logs"))
async def _(e):
    await getlogs(e)


########## AUTO ###########


@bot.on(events.NewMessage(incoming=True))
async def _(e):
    await thumb(e)


@bot.on(events.NewMessage(incoming=True))
async def _(e):
    await encod(e)


@app.on_message(filters.incoming & (filters.video | filters.document))
async def _(app, message):
    await pencode(message)


async def something():
    for i in itertools.count():
        await statuschecker()
        try:
            while LOCKFILE:
                await asyncio.sleep(2)
            if not WORKING and QUEUE:
                # user = int(OWNER.split()[0])
                file = list(QUEUE.keys())[0]
                name, user = QUEUE[list(QUEUE.keys())[0]]
                USER_MAN.clear()
                USER_MAN.append(user)
                try:
                    message = await app.get_messages(user, int(file))
                    mssg_r = await message.reply("`Downloading…`", quote=True)
                    e = await bot.send_message(user, reply_to=message.id, "`▼ Downloding Queue Files ▼`")
                except Exception:
                    message = ""
                    mssg_r = ""
                    e = await bot.send_message(user, "`▼ Downloding Queue Files ▼`")
                sender = await app.get_users(user)
                if LOG_CHANNEL:
                    log = int(LOG_CHANNEL)
                    op = await bot.send_message(
                        log,
                        f"[{sender.first_name}](tg://user?id={user}) `Currently Downloading A Queued Video…`",
                    )
                s = dt.now()
                try:
                    dl = "downloads/" + name
                    if message.text or is_url(file) is True:
                        pass
                    else:
                        download_task = await download2(dl, file, message, mssg_r)
                    wah = code(dl)
                    dl_info = await parse_dl(name)
                    ee = await e.edit(
                        f"{enmoji()} `Downloading…`{dl_info}",
                        buttons=[
                            [Button.inline("ℹ️", data=f"dl_stat{wah}")],
                            [Button.inline("CANCEL", data=f"cancel_dl{wah}")],
                        ],
                    )
                    if LOG_CHANNEL:
                        opp = await op.edit(
                            f"[{sender.first_name}](tg://user?id={user}) `Currently Downloading A Queued Video…`{dl_info}",
                            buttons=[
                                [Button.inline("ℹ️", data=f"dl_stat{wah}")],
                                [Button.inline("CANCEL", data=f"cancel_dl{wah}")],
                            ],
                        )
                    if message.text or is_url(file) is True:
                        if " " in message.text:
                            uri = message.text.split(" ", maxsplit=1)[1]
                        else: uri = message.text
                        if mssg_r:
                            await mssg_r.edit("`Downloading Torrent…`")
                        cmd = f"aria2c --seed-time=0 -d downloads {uri}"
                        process = await asyncio.create_subprocess_shell(
                            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                        )
                        stdout, stderr = await process.communicate()
                        if process.returncode != 0:
                            if DOWNLOAD_CANCEL:
                                if message:
                                    await mssg_r.edit(f"Download of `{name}` has been cancelled!")
                                await e.delete()
                                if LOG_CHANNEL:
                                    await op.edit(
                                        f"[{sender.first_name}'s](tg://user?id={user}) `Download has been cancelled.`",
                                    )
                                if QUEUE:
                                    QUEUE.pop(list(QUEUE.keys())[0])
                                DOWNLOAD_CANCEL.clear()
                                await save2db()
                                await qclean()
                                continue
                    try:
                        await download_task
                    except Exception:
                        pass
                    if DOWNLOAD_CANCEL:
                        if message:
                            await mssg_r.edit(
                                f"Download of `{name}` has been cancelled!"
                            )
                        await e.delete()
                        if LOG_CHANNEL:
                            await op.edit(
                                f"[{sender.first_name}'s](tg://user?id={user}) `Download has been cancelled.`",
                            )
                        if QUEUE:
                            QUEUE.pop(list(QUEUE.keys())[0])
                        DOWNLOAD_CANCEL.clear()
                        await save2db()
                        await qclean()
                        continue
                except Exception:
                    er = traceback.format_exc()
                    LOGS.info(er)
                    await channel_log(ers)
                    QUEUE.pop(list(QUEUE.keys())[0])
                    await save2db()
                    continue
                es = dt.now()
                kk = dl.split("/")[-1]
                if "[" in kk and "]" in kk:
                    pp = kk.split("[")[0]
                    qq = kk.split("]")[1]
                    kk = pp + qq
                else:
                    kk = kk
                aa = kk.split(".")[-1]
                rr = "encode"
                namo = dl.split("/")[1]
                if "v2" in namo:
                    name = namo.replace("v2", "")
                else:
                    name = namo
                bb, bb2 = await parse(name, kk, aa)
                out = f"{rr}/{bb}"
                b, d, c, rlsgrp = await dynamicthumb(name, kk, aa)
                tbcheck = Path("thumb2.jpg")
                if tbcheck.is_file():
                    thum = "thumb2.jpg"
                else:
                    thum = "thumb.jpg"
                with open("ffmpeg.txt", "r") as file:
                    # ffmpeg = file.read().rstrip()
                    nani = file.read().rstrip()
                    file.close()
                try:
                    if "This Episode" in nani:
                        bo = b
                        if d:
                            bo = f"Episode {d} of {b}"
                        if c:
                            bo += f" Season {c}"
                        nano = nani.replace(f"This Episode", bo)
                    else:
                        nano = nani
                except NameError:
                    nano = nani
                if "Fileinfo" in nano:
                    ffmpeg = nano.replace(f"Fileinfo", bb2)
                else:
                    ffmpeg = nano
                dtime = ts(int((es - s).seconds) * 1000)
                hehe = f"{out};{dl};{list(QUEUE.keys())[0]}"
                wah = code(hehe)
                if message:
                    await mssg_r.edit("`Waiting For Encoding To Complete`")
                nn = await e.edit(
                    "`Encoding Files…` \n**⏳This Might Take A While⏳**",
                    buttons=[
                        [Button.inline("📂", data=f"pres{wah}")],
                        [Button.inline("STATS", data=f"stats{wah}")],
                        [Button.inline("CANCEL PROCESS", data=f"skip{wah}")],
                    ],
                )
                if LOG_CHANNEL:
                    wak = await op.edit(
                        f"[{sender.first_name}](tg://user?id={user}) `Is Currently Encoding A Queued Video…`",
                        buttons=[
                            [Button.inline("📁", data=f"pres{wah}")],
                            [Button.inline("CHECK PROGRESS", data=f"stats{wah}")],
                            [Button.inline("CANCEL PROCESS", data=f"skip{wah}")],
                        ],
                    )
                cmd = ffmpeg.format(dl, out)
                if ALLOW_ACTION is True:
                    async with bot.action(user, "game"):
                        process = await asyncio.create_subprocess_shell(
                            cmd,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE,
                        )
                        stdout, stderr = await process.communicate()
                else:
                    process = await asyncio.create_subprocess_shell(
                        cmd,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    stdout, stderr = await process.communicate()
                er = stderr.decode()
                try:
                    if process.returncode != 0:
                        if len(stderr) > 4095:
                            yo = await app.send_message(user, "Uploading Error logs…")
                            out_file = "ffmpeg_error.txt"
                            with open("ffmpeg_error.txt", "w") as file:
                                file.write(str(stderr.decode()))
                                wrror = await yo.reply_document(
                                    document=out_file,
                                    force_document=True,
                                    quote=True,
                                    caption="`ffmpeg error`",
                                )
                            yo.delete()
                            os.remove(out_file)
                        else:
                            wrror = await nn.reply(stderr.decode())
                        nnn = await wrror.reply(
                            f"🔺 **Encoding of** `{bb2}` **Failed!**"
                        )
                        try:
                            os.remove(dl)
                        except Exception:
                            await nnn.reply("**Reason:** `Encoding Cancelled!`")
                        try:
                            await nn.delete()
                            await wak.delete()
                        except Exception:
                            pass
                        if QUEUE:
                            QUEUE.pop(list(QUEUE.keys())[0])
                        await save2db()
                        continue
                except BaseException:
                    er = traceback.format_exc()
                    LOGS.info(er)
                    LOGS.info(stderr.decode)
                    await channel_log(er)
                    await nn.edit("An Unknown error occurred waiting for 30 seconds before trying again. ")
                    if LOG_CHANNEL:
                        await wak.edit("An unknown error occurred waiting for 30 seconds before trying again.")
                    await asyncio.sleep(30)
                    await qclean()
                    continue 
                ees = dt.now()
                time.time()
                try:
                    await nn.delete()
                    await wak.delete()
                except Exception:
                    pass
                if message:
                    nnn = mssg_r
                else:
                    tex = "`▲ Uploading ▲`"
                    nnn = await app.send_message(chat_id=e.chat_id, text=tex)
                fname = out.split("/")[1]
                tbcheck = Path("thumb2.jpg")
                if tbcheck.is_file():
                    thum = "thumb2.jpg"
                else:
                    thum = "thumb.jpg"
                pcap = await custcap(name, fname)
                if message:
                    ds = await upload2(e.chat_id, out, nnn, thum, pcap, message)
                else:
                     ds = await upload2(e.chat_id, out, nnn, thum, pcap)
                await nnn.delete()
                if FCHANNEL:
                    chat = int(FCHANNEL)
                    await ds.copy(chat_id=chat)
                if LOG_CHANNEL:
                    chat = int(LOG_CHANNEL)
                    await ds.copy(chat_id=chat)
                org = int(Path(dl).stat().st_size)
                com = int(Path(out).stat().st_size)
                pe = 100 - ((com / org) * 100)
                per = str(f"{pe:.2f}") + "%"
                eees = dt.now()
                x = dtime
                xx = ts(int((ees - es).seconds) * 1000)
                xxx = ts(int((eees - ees).seconds) * 1000)
                try:
                    a1 = await info(dl, e)
                    text = ""
                    if rlsgrp:
                        text += f"**Source:** `[{rlsgrp}]`"
                    text += f"\n\nMediainfo: **[(Source)]({a1})**"
                    dp = await ds.reply(
                        text,
                        disable_web_page_preview=True,
                        quote=True,
                    )
                    if LOG_CHANNEL:
                        await dp.copy(chat_id=chat)
                except Exception:
                    pass
                dk = await ds.reply(
                    f"**Encode Stats:**\n\nOriginal Size : {hbs(org)}\nEncoded Size : {hbs(com)}\nEncoded Percentage : {per}\n\nDownloaded in {x}\nEncoded in {xx}\nUploaded in {xxx}",
                    disable_web_page_preview=True,
                    quote=True,
                )
                if LOG_CHANNEL:
                    await dk.copy(chat_id=chat)
                QUEUE.pop(list(QUEUE.keys())[0])
                await save2db()
                os.system("rm -rf thumb2.jpg")
                os.remove(dl)
                os.remove(out)
            else:
                await asyncio.sleep(3)
        except Exception:
            er = traceback.format_exc()
            LOGS.info(er)
            await channel_log(ers)


########### Start ############

LOGS.info("Bot has started.")
with bot:
    bot.loop.run_until_complete(startup())
    bot.loop.run_until_complete(something())
    bot.loop.run_forever()
