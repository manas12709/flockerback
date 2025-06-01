# monkey patch BEFORE imports
import eventlet
eventlet.monkey_patch()

from main import app
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

# Setup SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Track users by room
online_users = {}

def get_avatar(username):
    # Placeholder logic, replace with real logic if using avatars from database
    return f"https://api.dicebear.com/7.x/identicon/svg?seed={username}"

@socketio.on("join")
def handle_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)

    # Add user to room's online list
    if room not in online_users:
        online_users[room] = set()
    online_users[room].add(username)

    # Notify room
    emit("message", {
        "username": "System",
        "msg": f"{username} has joined the room.",
        "timestamp": datetime.now().strftime("%H:%M"),
        "avatar": ""
    }, room=room)

    # Send updated online user list
    emit("online_users", list(online_users[room]), room=room)

@socketio.on("send_message")
def handle_send_message(data):
    username = data["username"]
    room = data["room"]
    msg = data["msg"]

    emit("message", {
        "username": username,
        "msg": msg,
        "timestamp": datetime.now().strftime("%H:%M"),
        "avatar": get_avatar(username)
    }, room=room)

@socketio.on("leave")
def handle_leave(data):
    username = data["username"]
    room = data["room"]
    leave_room(room)

    if room in online_users:
        online_users[room].discard(username)

    emit("message", {
        "username": "System",
        "msg": f"{username} has left the room.",
        "timestamp": datetime.now().strftime("%H:%M"),
        "avatar": ""
    }, room=room)

    emit("online_users", list(online_users[room]), room=room)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8505)
