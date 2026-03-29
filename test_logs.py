#!/usr/bin/env python3
"""
Test script to trigger a request and generate logs for observability testing.
"""

import asyncio
import websockets
import json


async def test_request():
    uri = "ws://localhost:42002/ws/chat?access_key=raspberry-ink-unified"

    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket")

            # Send a request that will trigger backend API calls
            message = {"type": "text", "content": "What labs are available in the LMS?"}

            print("📤 Sending request:", message["content"])
            await websocket.send(json.dumps(message))

            # Wait for response
            response = await websocket.recv()
            print("📥 Response received")
            print(f"Response length: {len(response)} characters")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_request())
