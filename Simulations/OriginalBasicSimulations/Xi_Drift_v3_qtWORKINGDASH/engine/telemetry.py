import asyncio
import websockets
import json

async def handler(ws, path):
    print(f"📡 New client connected from {ws.remote_address}")
    try:
        while True:
            await asyncio.sleep(1)
            telemetry = {
                "frame": 42,
                "drift": 0.015,
                "entropy": 2.718
            }
            await ws.send(json.dumps(telemetry))
    except websockets.ConnectionClosed:
        print("⚠️ WebSocket client disconnected")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("📡 Telemetry WebSocket running at ws://0.0.0.0:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
