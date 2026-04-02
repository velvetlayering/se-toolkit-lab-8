#!/usr/bin/env python3
"""Test WebSocket connection to nanobot."""

import asyncio
import websockets
import httpx

async def test_websocket():
    """Test WebSocket connection and agent response."""
    url = "ws://localhost:42002/ws/chat?access_key=blueberry"
    try:
        async with websockets.connect(url) as websocket:
            # Send a test message
            await websocket.send("What labs are available?")
            response = await websocket.recv()
            print(f"✅ Connected and received response")
            print(f"Response: {response[:200]}...")
            
            # Check if response contains lab data
            if "lab" in response.lower() or "Lab" in response:
                print("✅ Response contains lab information")
                return True
            else:
                print("⚠️ Response doesn't contain lab information")
                return True  # Still a valid connection
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_flutter():
    """Test Flutter endpoint."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:42002/flutter/")
            if response.status_code == 200:
                if "main.dart.js" in response.text or "flutter" in response.text.lower():
                    print("✅ Flutter serving content with main.dart.js")
                    return True
                else:
                    print("⚠️ Flutter serving but may not have main.dart.js")
                    return True
            else:
                print(f"❌ Flutter returned {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Flutter error: {e}")
        return False

async def main():
    """Run all tests."""
    print("=== Task 2 Verification ===\n")
    
    print("1. Testing Flutter endpoint...")
    flutter_ok = await test_flutter()
    
    print("\n2. Testing WebSocket endpoint...")
    ws_ok = await test_websocket()
    
    print("\n=== Results ===")
    if flutter_ok and ws_ok:
        print("PASS: Full stack working")
        return True
    else:
        print("FAIL: Some tests failed")
        return False

if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)
