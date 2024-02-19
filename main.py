import websockets
import json
import asyncio
import aiohttp
import traceback

instance = "msky.nekokawa.net"
token = "とーくん"
url = f"wss://{instance}/streaming?i={token}"


async def heartbeat(ws):
    while True:
        try:
            await asyncio.sleep(60)
            await ws.send("h")
            continue
        except websockets.exceptions.ConnectionClosedError:
            print("websocketsの嘘つき！")
            pass
        except:
            print(traceback.format_exc())
            pass


async def receive(ws):
    while True:
        try:
            data = json.loads(await ws.recv())
            if data["body"]["type"] == "note":
                note = data["body"]["body"]
                if note['text']:
                    if len(note['mentions']) > 3:
                        # 殺害
                        data = {
                            "i": token,
                            "userId": note['user']['id']
                        }
                        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as session:
                            await session.post(f"https://{instance}/api/admin/delete-account", json=data)
                        # インスタンスブロック
                        data = {
                            "allowPartial": True,
                            "blocked": True,
                            "i": token,
                            "limit": 100
                        }
                        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as session:
                            r = await session.post(f"https://{instance}/api/federation/instances", json=data)
                            blocked_instances = await r.json()
                        block_list = []
                        for blocked_instance in blocked_instances:
                            block_list.append(blocked_instance['host'])
                        block_list.append(note['user']['host'])
                        data = {
                            "blockedHosts": block_list,
                            "i": token
                        }
                        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as session:
                            await session.post(f"https://{instance}/api/admin/update-meta", json=data)
                        # 報告
                        notedata = {
                            'i': token,
                            'text': f"{note['user']['host']}の荒らしを殺害:yougotthis:",
                        }
                        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as session:
                            await session.post(f"https://{instance}/api/notes/create", json=notedata)
                        print(f"{note['user']['host']}の荒らしを殺害:yougotthis:")
                        break
            # print(data)
        except websockets.exceptions.ConnectionClosedError:
            print("websocketsの嘘つき！")
            pass
        except:
            print(traceback.format_exc())
            pass


async def runner():
    global url
    async with websockets.connect(url) as ws:
        print("streaming APIに接続しました。")
        await ws.send(json.dumps({
                "type": "connect",
                "body": {
                    "channel": "main",
                    "id": "receive"
                }
            }))
        await ws.send(json.dumps({
            "type": "connect",
            "body": {
                "channel": "globalTimeline",
                "id": "receive",
                "params": {
                    "withReplies": True
                }
            }
        }))
        print("グローバルタイムラインに接続しました。")
        await asyncio.gather(
            heartbeat(ws),
            receive(ws),
        )


asyncio.get_event_loop().run_until_complete(runner())
