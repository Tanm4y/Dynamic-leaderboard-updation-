from flask import Flask, render_template, request, jsonify
from flask_sock import Sock
import json

from .leaderboard import Leaderboard
from .topologymgr import BinTreeTopologyManager
from .notifbus import NotificationBus
from .messaging import MessagingTask

app = Flask(__name__)
sock = Sock(app)

app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 20}

leaderboard = Leaderboard()
clients = []

def notify_all(data):
    for ws in clients[:]:
        try:
            ws.send(data)
        except Exception as e:
            print("Error sending to client:", e, flush=True)
            clients.remove(ws)  # Remove disconnected clients

notifs = NotificationBus(BinTreeTopologyManager(None), leaderboard, notify_all)
mt = MessagingTask(notifs, app)

def notify_all_except(data, conn):
    for ws in clients[:]:
        if ws is conn: continue
        try:
            ws.send(data)
        except Exception as e:
            print("Error sending to client:", e, flush=True)
            clients.remove(ws)  # Remove disconnected clients

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    leaderboard_data = leaderboard.get_leaderboard()
    return jsonify(leaderboard_data)

@app.route('/api/update', methods=['POST'])
def update_leaderboard():
    player_data = request.get_json()
    leaderboard.update(player_data['name'], player_data['score'])

    # Broadcast the update to all WebSocket clients
    leaderboard_data = json.dumps({"op": "lb_update", "d": player_data})
    notify_all(leaderboard_data)
    mt.conn and mt.send(leaderboard_data)

    return jsonify({'message': 'Leaderboard updated successfully!'})

@sock.route('/connect')
def leaderboard_ws(ws):
    # Add the WebSocket connection to the clients list
    clients.append(ws)
    try:
        # Send the current leaderboard data upon connection
        ws.send(json.dumps({"op": "lb_sync", "d": leaderboard.get_leaderboard()}))
        ws.send(json.dumps({"op": "tm_sync", "d": notifs.tm.serialize()}))

        # Keep the connection open to listen for incoming messages or disconnection
        while True:
            message = ws.receive()
            if message is None:
                break  # Exit if the client disconnects
            p = json.loads(message)
            print("received from child", ws, p, flush=True)
            data = p["d"]
            op = p["op"]

            if op == "lb_update":
                notifs.lb.update(data["name"], data["score"])
                mt.conn and mt.send(message) # forward to parent
            elif op == "tm_update":
                notifs.tm.update(data)
            elif op == "tm_sync":
                notifs.tm.update_with(data)
            elif op == "lb_sync":
                notifs.lb.players.update({d["name"]: d["score"] for d in data})

            notify_all_except(message, ws)
    finally:
        # Remove the client from the list upon disconnection
        clients.remove(ws)

@app.route('/')
def index():
    return render_template('leaderboard.html')

mt.start()

def main():
    app.run()
    mt.join()

if __name__ == "__main__":
    main()