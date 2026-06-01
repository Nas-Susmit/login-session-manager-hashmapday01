#!/usr/bin/env python3
"""
Demonstrates O(1) token validation flow.
"""

import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def test_login():
    """Test login and token generation."""
    print("\n[1] POST /login — Valid credentials")
    resp = requests.post(f"{BASE_URL}/login", json={
        "username": "demo",
        "password": "pass"
    })
    print(f"    Status: {resp.status_code}")
    print(f"    Response: {resp.json()}")
    return resp.json().get("token")

def test_login_invalid():
    """Test login with invalid credentials."""
    print("\n[2] POST /login — Invalid credentials")
    resp = requests.post(f"{BASE_URL}/login", json={
        "username": "hacker",
        "password": "wrong"
    })
    print(f"    Status: {resp.status_code}")
    print(f"    Response: {resp.json()}")

def test_protected(token):
    """Test protected route with valid token."""
    print("\n[3] GET /protected — Valid token")
    resp = requests.get(f"{BASE_URL}/protected", headers={
        "Authorization": token
    })
    print(f"    Status: {resp.status_code}")
    print(f"    Response: {resp.json()}")

def test_protected_invalid():
    """Test protected route with invalid token."""
    print("\n[4] GET /protected — Invalid token")
    resp = requests.get(f"{BASE_URL}/protected", headers={
        "Authorization": "fake-token-123"
    })
    print(f"    Status: {resp.status_code}")
    print(f"    Response: {resp.json()}")

def test_logout(token):
    """Test logout — removes token from HashMap."""
    print("\n[5] POST /logout")
    resp = requests.post(f"{BASE_URL}/logout", headers={
        "Authorization": token
    })
    print(f"    Status: {resp.status_code}")
    print(f"    Response: {resp.json()}")

def test_protected_after_logout(token):
    """Verify token is invalidated after logout."""
    print("\n[6] GET /protected — After logout (token should be invalid)")
    resp = requests.get(f"{BASE_URL}/protected", headers={
        "Authorization": token
    })
    print(f"    Status: {resp.status_code}")
    print(f"    Response: {resp.json()}")

def test_stats():
    """Check active session count."""
    print("\n[7] GET /stats — Active sessions")
    resp = requests.get(f"{BASE_URL}/stats")
    print(f"    Status: {resp.status_code}")
    print(f"    Response: {resp.json()}")

if __name__ == "__main__":
    print("=" * 60)
    print("  Testing HashMap Session Manager")
    print("=" * 60)
    print("Make sure the server is running: python session_manager.py")
    print("=" * 60)

    test_login_invalid()
    token = test_login()
    if token:
        test_protected(token)
        test_protected_invalid()
        test_stats()
        test_logout(token)
        test_protected_after_logout(token)
        test_stats()

    print("\n" + "=" * 60)
    print("  All tests completed!")
    print("=" * 60)
