# telemetry.py
import asyncio
import websockets
import os


async def handler(ws, path):  # ✅ Add `path` argument
    print("📡 New client connected.")
    await ws.send("🛰️ Telemetry online...")
    try:
        while True:
            await asyncio.sleep(1)
            await ws.send("📊 Drift value: 0.021 | Entropy: 1.234")
    except websockets.exceptions.ConnectionClosed:
        print("❌ Client disconnected.")

async def main():
    print("📡 Telemetry WebSocket running at ws://0.0.0.0:8765")
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
