from flask import Flask, request, jsonify
import uuid
import time
import threading

app = Flask(__name__)

# ============================================================
# HashMap in Action: sessions[token] = {"user": str, "expiry": float}
# ============================================================
sessions = {}  # Python dict = HashMap
# Key: token (str), Value: {"user": str, "expiry": timestamp}
# All operations (set, get, delete) are O(1) average time complexity

def clean_expired():
    """Background thread that removes expired sessions every 60 seconds."""
    while True:
        now = time.time()
        # O(n) scan to find expired tokens — acceptable since cleanup is infrequent
        expired = [t for t, v in sessions.items() if v['expiry'] < now]
        for t in expired:
            sessions.pop(t, None)
        time.sleep(60)

# Start background cleanup thread
cleanup_thread = threading.Thread(target=clean_expired, daemon=True)
cleanup_thread.start()

@app.route('/login', methods=['POST'])
def login():
    """
    POST /login
    Accepts: {"username": str, "password": str}
    Returns: {"token": str} on success, 401 on failure

    O(1) insert into HashMap — scales to millions of sessions.
    """
    data = request.get_json()

    # Mock credential check (in production: hash comparison)
    if data.get('username') == 'demo' and data.get('password') == 'pass':
        token = str(uuid.uuid4())
        sessions[token] = {
            'user': data['username'],
            'expiry': time.time() + 1800  # 30 minutes TTL
        }
        return jsonify({'token': token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/protected', methods=['GET'])
def protected():
    """
    GET /protected
    Header: Authorization: <token>
    Returns: {"message": str} on success, 401 on failure

    O(1) token lookup from HashMap — no linear scan needed.
    """
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'error': 'Missing token'}), 401

    # O(1) HashMap lookup — key is hashed, bucket found in constant time
    session = sessions.get(token)

    if not session or session['expiry'] < time.time():
        return jsonify({'error': 'Invalid or expired session'}), 401

    return jsonify({'message': f'Welcome {session["user"]}!'}), 200

@app.route('/logout', methods=['POST'])
def logout():
    """
    POST /logout
    Header: Authorization: <token>
    Returns: {"message": str}

    O(1) deletion from HashMap — immediate invalidation.
    """
    token = request.headers.get('Authorization')
    sessions.pop(token, None)  # O(1) remove
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/stats', methods=['GET'])
def stats():
    """Debug endpoint: show active session count."""
    return jsonify({'active_sessions': len(sessions)}), 200

if __name__ == '__main__':
    print("=" * 60)
    print("  HashMap Session Manager — Flask MVP")
    print("=" * 60)
    print("Endpoints:")
    print('  POST /login      → Body: {"username":"demo","password":"pass"}')
    print("  GET  /protected  → Header: Authorization: <token>")
    print("  POST /logout     → Header: Authorization: <token>")
    print("  GET  /stats      → Show active session count")
    print("=" * 60)
    print("Running on http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)
