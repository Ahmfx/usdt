from os import system, name, path
from random import choice
from asyncio import run
from requests import get
from telethon import TelegramClient, errors, functions
from telethon.sessions import StringSession
from telethon.tl.functions.account import CheckUsernameRequest
from telethon.tl.functions.channels import UpdateUsernameRequest, DeleteChannelRequest, CreateChannelRequest
from bs4 import BeautifulSoup as S
from telebot import TeleBot

token = "7328640668:AAEsU8BL-vgYGVr9mwoAAj63UduZ57fzh-M" # توكنك
id = "1451542769" # ايديك

def usernames():
    k = ''.join(choice('qwertyuiopasdfghjklzxcvbnm') for i in range(1))
    n = ''.join(choice('qwertyuiopasdfghjklzxcvbnm1234567890') for i in range(1))
    c = ''.join(choice('qwertyuiopasdfghjklzxcvbnm1234567890') for i in range(1))
    z = ''.join(choice('qwertyuiopasdfghjklzxcvbnm1234567890') for i in range(1))
    g = ''.join(choice('qwertyuiopasdfghjklzxcvbnm1234567890') for i in range(1))
    _ = ''.join("_")
    e = ''.join(choice('qwertyuiopasdfghjklzxcvbnm') for i in range(1))
    u1 = k + c + e + e + e
    u2 = k + z + z + z + n
    u3 = k + k + k + n + c
    u4 = n + n + _ + n + c
    u5 = n + c + n + _ + n
    u6 = n + c + n + c + n + n + n + n
    u7 = n + c + n + c + c + c + c + c
    u8 = n + n + n + k + k + k + k + n 
    u9 = n + n + k + k + k + k + k + k
    u10 = n + k + n + n + n + k + n
    u11 = k + n + n + n + n + n + k
    u12 = k + n + k + n + k + n + k
    u13 = k + k + k + k + k + n + n
    u14 = k + k + k + k + k + k + k + n
    u15 = n + k + k + k + k + k + k + k
    u16 = n + n + n + n + k + k + k + k
    u17 = n + n + k + k + k + k + k + k
    u18 = k + k + k + n + n + k + k + k
    s = u1,u2,u3,u4,u5,u6,u7,u8,u9,u10,u11,u12,u13,u14,u15,u16,u17,u18
    return choice(s)

async def channels2(client, username):
    async for chat in client.iter_dialogs():
        if chat.name == f'[ {username} ]' and not chat.entity.username:
            await client(DeleteChannelRequest(channel=chat.entity))
            print('- Flood : ' + username + ' .')
            return False
    return True

async def fragment(username):
    response = get("https://fragment.com/username/{}".format(str(username))).text
    soup = S(response, 'html.parser')
    ok = soup.find("meta", property="og:description").get("content")
    if "An auction to get the Telegram" in ok or "Telegram and secure your ownership" in ok or "Check the current availability of" in ok or "Secure your name with blockchain in an ecosystem of 700+ million users" in ok:
        return True
    elif "is taken" in ok:
        return "is taken"
    else:
        return False

async def telegram(client, claim, username):
    global token,id
    if claim:
        text = f"‹ Done Save UserName ›\n‹ UserName → @{username} ›"
    else:
        text = f"‹ New UserName Flood ›\n‹ UserName → @{username} ›"
    try:
        TeleBot(token=token).send_message(id,text=text)
    except Exception:pass
    await client.send_message('me', text)

async def claimed(client, username):
    result = await client(CreateChannelRequest(
                title=f'Claim [ {username} ]',
        about=f'',
        megagroup=False))
    try:
        await client(UpdateUsernameRequest(channel=result.chats[0], username=username))
        await client.send_message(username, f'‹ Done Save UserName ›\n‹ UserName → @{username} ›')
        return True
    except Exception as e:
        await client.send_message("me", f'⌯ Error Message .\nMessage : {e} .')
        return False

async def checker(username, client):
    try:
        check = await client(CheckUsernameRequest(username=username))
        if check:
            print('- Available : ' + username + ' .')
            claimer = await claimed(client, username)
            claim = claimer and (await fragment(username)) == "is taken"
            print('- Claimer ? ' + str(claim) + '\n' + '_ ' * 20)
            flood = await channels2(client, username)
            if not flood:
                
                with open('flood.txt', 'a') as floodX: floodX.write(username + "\n")
            else:
                print('- Taken : ' + username + ' .')
            await telegram(client,claim,username)
    except errors.rpcbaseerrors.BadRequestError:
        print('- Banned : ' + username + ' .')
        with open("banned4.txt", "a") as file:
            file.write(username + '\n')
    except errors.FloodWaitError as timer:
        print(f'- Flood Account [ {timer.seconds} Seconds ] .')
    except errors.UsernameInvalidError:
        print('- Error : ' + username + ' .')

async def start(client, username):
    try:
        ok = await fragment(username)
    except:
        return
    try:
        if not ok:
            await checker(username, client)
        elif ok == "is taken":
            print('- Taken : ' + username + ' .')
        else:
            print('- Fragment : ' + username + ' .')
            with open("fragment.txt", "a") as frag_file:
                frag_file.write(username + '\n')
    except Exception as e:
        print(e)

async def clienT():
    global sessionL
    try:
        client = TelegramClient(StringSession(sessionL), "25324581", "08feee5eeb6fc0f31d5f2d23bb2c31d0")
        await client.start()
    except:
        exit()
    system('cls' if name == 'nt' else 'clear')
    return client

async def main():
    client = await clienT()
    if not path.exists('banned4.txt'): open('banned4.txt', 'w').close()
    if not path.exists('flood.txt'): open('flood.txt', 'w').close()
    if not path.exists('fragment.txt'): open('fragment.txt', 'w').close()
    while True:
        username = usernames()
        file1 = open('banned4.txt', 'r').read() or ''
        file2 = open('fragment.txt', 'r').read() or ''
        if username in file1:
            print('- Banned : ' + username + ' .')
            continue
        if username in file2:
            print('- Fragment : ' + username + ' .')
            continue
        await start(client, username)

sessionL = input('[+] Enter Session : ')
run(main())
