#!/usr/bin/env python3
"""Test agent with observability question."""

import asyncio
import websockets

async def test_observability():
    """Test agent with observability question."""
    url = "ws://localhost:42002/ws/chat?access_key=blueberry"
    try:
        async with websockets.connect(url) as websocket:
            # Send observability question
            await websocket.send("Any errors in the system in the last hour?")
            response = await websocket.recv()
            print(f"✅ Connected and received response")
            print(f"Response: {response[:500]}...")
            return response
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    result = asyncio.run(test_observability())
    print("\n" + "="*50)
    if result:
        print("PASS: Agent responded to observability question")
    else:
        print("FAIL: Agent did not respond")
