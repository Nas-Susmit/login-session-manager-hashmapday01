# 🔐 HashMap Session Manager — Flask MVP

A minimal, single-file session manager demonstrating **HashMap O(1) operations** in a real-world authentication flow. Built for DSA interview prep and portfolio showcases.

---

## 🎯 Why HashMap?

| Operation | Without HashMap (List) | With HashMap (Dict) |
|-----------|----------------------|---------------------|
| Token lookup | O(n) linear scan | **O(1)** average |
| Insert session | O(1) append | **O(1)** average |
| Delete session | O(n) search + remove | **O(1)** average |

In production, Redis, in-memory caches, and session stores all use **hashing** under the hood for exactly this reason.

---

## 🚀 Quick Start

```bash
# 1. Install Flask
pip install flask

# 2. Run the server
python session_manager.py

# 3. Test with curl (or use the test script)
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"pass"}'

# 4. Use the returned token
curl -X GET http://127.0.0.1:5000/protected \
  -H "Authorization: <your-token>"
```

---

## 📡 API Endpoints

| Endpoint | Method | Headers | Body | Response |
|----------|--------|---------|------|----------|
| `/login` | POST | — | `{"username","password"}` | `{"token": "..."}` |
| `/protected` | GET | `Authorization: <token>` | — | `{"message": "Welcome demo!"}` |
| `/logout` | POST | `Authorization: <token>` | — | `{"message": "Logged out"}` |
| `/stats` | GET | — | — | `{"active_sessions": N}` |

---

## 🧠 DSA Concepts Demonstrated

- **HashMap / Hash Table**: Python `dict` provides O(1) average for `get`, `set`, `delete`
- **UUID Generation**: `uuid.uuid4()` for collision-resistant tokens
- **TTL / Expiry**: Time-based invalidation without external DB
- **Background Cleanup**: Daemon thread for periodic garbage collection
- **Thread Safety**: Single-threaded Flask dev server; production uses WSGI

---

## 🔮 Next Steps

- [ ] **Sliding Expiration**: Refresh TTL on every `/protected` hit
- [ ] **Rate Limiting**: Another HashMap tracking `ip → request_count`
- [ ] **Switch to `cachetools.TTLCache`**: Auto-expiry without manual cleanup
- [ ] **Redis Backend**: Replace in-memory dict with distributed hash store
- [ ] **JWT Integration**: Sign tokens instead of storing in memory

---


---

## 📁 Files

| File | Description |
|------|-------------|
| `session_manager.py` | Main Flask application |
| `test_session_manager.py` | API test script |
| `README.md` | This file |

---

*Built for placement season prep. Grind DSA, build projects, land offers.* 🚀
