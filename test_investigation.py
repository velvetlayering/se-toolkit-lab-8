#!/usr/bin/env python3
"""Test the agent's investigation capabilities for Task 4A."""

import asyncio
import json
import websockets
import urllib.parse


async def test_investigation():
    # WebSocket endpoint with access key
    uri = "ws://localhost:42002/ws/chat?access_key=raspberry-ink-unified"

    try:
        async with websockets.connect(uri) as websocket:
            print("🔗 Connected to nanobot WebSocket")

            # First trigger a failure by asking about labs (this will hit the LMS backend)
            print("📤 Asking about labs to trigger backend call...")
            trigger_message = {"text": "What labs are available?"}
            await websocket.send(json.dumps(trigger_message))

            # Read the response
            response = await websocket.recv()
            response_data = json.loads(response)
            print("📥 Response to labs query:")
            print(
                f"Content: {response_data['content'][:200]}..."
            )  # Show first 200 chars

            # Wait a moment for logs to be processed
            await asyncio.sleep(2)

            # Now ask "What went wrong?" to trigger investigation
            print("\n🔍 Now asking 'What went wrong?' to test investigation...")
            investigation_message = {"text": "What went wrong?"}
            await websocket.send(json.dumps(investigation_message))

            # Read the investigation response
            investigation_response = await websocket.recv()
            investigation_data = json.loads(investigation_response)
            print("\n📋 INVESTIGATION RESPONSE:")
            print("=" * 60)
            print(investigation_data["content"])
            print("=" * 60)

            return investigation_data["content"]

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    result = asyncio.run(test_investigation())
    if result:
        print(f"\n✅ Investigation test completed successfully")
    else:
        print("\n❌ Investigation test failed")
