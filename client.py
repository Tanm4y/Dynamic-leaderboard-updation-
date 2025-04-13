import websocket
import json
import time

def on_message(ws, message):
    print("Received update from server:")
    leaderboard = json.loads(message)
    for player in leaderboard:
        print(f"{player['name']}: {player['score']}")

def on_error(ws, error):
    print("WebSocket Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed")

def on_open(ws):
    print("Connected to the WebSocket server")

if __name__ == "__main__":
    # WebSocket server URL
    ws_url = "ws://127.0.0.1:5000/connect"

    # Create WebSocket app
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    # Run WebSocket app with reconnection logic
    while True:
        ws.run_forever()
        print("Reconnecting in 2 seconds...")
        time.sleep(2)  # Wait before reconnecting
