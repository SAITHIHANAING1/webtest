#!/usr/bin/env python3
"""
Run SafeStep Flask app on local network for mobile testing
"""

import socket
from app import app

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote address to get local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    local_ip = get_local_ip()
    port = 5000
    
    print(f"📱 Access from your phone: http://{local_ip}:{port}")
    print(f" Access from this computer: http://localhost:{port}")
    print("⚠️  Make sure your phone is on the same WiFi network")
    print("\n🔗 Demo login URL for phone:")
    print(f"   http://{local_ip}:{port}/login")
    print("\n📍 Location sharing URL for phone:")
    print(f"   http://{local_ip}:{port}/caregiver/zones/share?pid=demo")
    print("\n" + "="*60)
    
    app.run(
        host="0.0.0.0",  # Listen on all network interfaces
        port=port,
        debug=True
    )
