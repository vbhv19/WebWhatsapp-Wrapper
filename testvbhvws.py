import asyncio
import websockets

qs = "s%253A3_UKy_5H0UPhADbj9d7zHXeBRY_wkKX0.vqbocQU2L%252F6NNTPtmEvW%252BYmvcuNmGwPQB0NkEWiAtVA&reqver=12.19&reqsrc=android&reqdev=OnePlus%7CONEPLUS%20A5000%7CAndroid%7C9&prodId=1&uuid=a58383f1d00a35fb&mod=ONEPLUS%20A5000&brand=OnePlus&osver=9&jsver=49&apntkn=c0zQDW0lI8Y:APA91bE5cVx_g7IEu-H_N1wz32ddxk1RWKaCYQ65Dlszi-_KWQV1nMVwIjNxMcprjGt9lJhdaFXNZXitdW-z8dU6VxiILf2SLyONuC-Q1YekEJAPd7JL1YviS0Ewy0i9vuEqXm57pj70"

async def hello():
    async with websockets.connect(
            'ws://192.168.31.12:9099/wss?cookie=' + qs) as websocket:
        greeting = await websocket.recv()
        print(greeting)

hello()
# asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()