import asyncio
import json

import websockets


async def check_permit(websocket):
    send_text = "puti"
    await websocket.send(send_text)
    return True


async def recv_msg(websocket):

    while 1:
        recv_text = await websocket.recv()
        res = json.loads(recv_text)
        common = res["common"]
        method = common["method"]
        room_id = common["roomId"]
        if method == "WebcastChatMessage":  # 聊天
            content = res["content"]
            nickname = res["user"]["nickname"]
            print(f"[{room_id}]{nickname}说：{content}")


async def main_logic(websocket, path):
    await check_permit(websocket)
    await recv_msg(websocket)


start_server = websockets.serve(main_logic, "127.0.0.1", 9999)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
