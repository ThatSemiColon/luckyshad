import asyncio
import os

import requests
from pyrogram import Client, filters
from pyrogram.types import Message

bot = Client(
    "CW",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH"),
)


@bot.on_message(filters.command(["start"]))
async def start(bot: Client, update: Message):
    await update.reply_text(
        "Hi i am **physics wallah Downloader**.\n\n"
        "**NOW:-** Press **/login** to continue..\n\n"
    )


@bot.on_message(filters.command(["login"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(
        "Send **Auth code** in this manner otherwise bot will not respond.\n\n"
        "Send like this:-  **AUTH CODE**"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text1 = input1.text
    headers = {
        "Host": "api.penpencil.xyz",
        "authorization": f"Bearer {raw_text1}",
        "client-id": "5f439b64d553cc02d283e1b4",
        "client-version": "19.0",
        "user-agent": "Android",
        "randomid": "987daa96a6200e17",
        "client-type": "MOBILE",
        "device-meta": "{APP_VERSION:19.0,DEVICE_MAKE:Asus,DEVICE_MODEL:ASUS_X00TD,OS_VERSION:6,PACKAGE_NAME:xyz.penpencil.khansirofficial}",
        "content-type": "application/json; charset=UTF-8",
    }

    params = {
        "mode": "2",
        "filter": "false",
        "exam": "",
        "amount": "",
        "organisationId": "5f439b64d553cc02d283e1b4",
        "classes": "",
        "limit": "20",
        "page": "1",
        "programId": "5f476e70a64b4a00ddd81379",
        "ut": "1652675230446",
    }
    await m.reply_text("**You have these Batches :-\n\nBatch ID : Batch Name**")
    aa = ""
    response = requests.get(
        "https://api.penpencil.co/v3/batches/my-batches", params=params, headers=headers
    ).json()["data"]
    for data in response:
        batch_name = data["name"]
        batch_id = data["_id"]
        aa = aa + f"**{batch_name}**  :  ```{batch_id}```\n\n"
    await m.reply_text(aa)

    await m.reply_text("**Now send the Batch ID to Download**")
    input3 = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    response2 = requests.get(
        f"https://api.penpencil.co/v3/batches/{raw_text3}/details", headers=headers
    ).json()["data"]["subjects"]

    await m.reply_text("Subject : Subject_Id")
    bb = ""
    for data in response2:
        subject_name = data["subject"]
        subject_id = data["_id"]
        bb = bb + f"**{subject_name}**  :  ```{subject_id}```\n\n"
    await m.reply_text(bb)

    await m.reply_text("**Now send the subject ID to Download**")
    input4 = await bot.listen(editable.chat.id)
    raw_text4 = input4.text

    await m.reply_text(
        "**Now Send Content Type you want to extract.**\n```DppNotes```|```videos```|```notes```"
    )
    input5 = await bot.listen(editable.chat.id)
    raw_text5 = input5.text

    xx = await m.reply_text("Genrating Course txt in this id")
    to_write = ""
    for z in range(1, 15):  # max 15 pages
        params1 = {
            "page": f"{z}",
            "tag": "",
            "contentType": f"{raw_text5}",
        }

        response3 = requests.get(
            f"https://api.penpencil.co/v2/batches/{raw_text3}/subject/{raw_text4}/contents",
            params=params1,
            headers=headers,
        ).json()["data"]

        if raw_text5 == "videos":
            for data in response3:
                try:
                    url = (
                        f"https://psitoffers.store/testkey.php?vid={data['url'].split('/')[-2]}&quality=720"
                        if raw_text5 == "videos"
                        else f"{data['baseUrl']}{data['key']}"
                    )
                    topic = data["topic"]
                    write = f"{topic} {url}\n"
                    to_write = to_write + write
                except Exception:
                    pass
        else:  # for notes + dpps
            for i in range(len(response3)):
                try:
                    c = response3[i]
                    b = c["homeworkIds"][0]
                    a = b["attachmentIds"][0]
                    name = response3[i]["homeworkIds"][0]["topic"].replace("|", " ").replace(":", " ")
                    url = a["baseUrl"] + a["key"]
                    write = f"{name} {url}\n"
                    to_write = to_write + write
                except Exception:
                    pass

    out_file = f"{raw_text5} {raw_text4}.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(to_write)

    with open(out_file, "rb") as f:
        await asyncio.sleep(5)
        await m.reply_document(document=f, caption="Here is your txt file.")
        await xx.delete(True)


if __name__ == "__main__":
    bot.run()
