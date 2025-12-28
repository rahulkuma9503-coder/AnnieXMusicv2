import os
import sys
import socket
import threading

# Minimal port binding for Render - MUST BE FAST
PORT = int(os.getenv('PORT', 10000))

def bind_port_immediately():
    try:
        # Create socket and bind in one step
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', PORT))
        s.listen(5)
        
        # Pre-generated HTTP response
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Connection: close\r\n\r\n"
            "Annie Music Bot is starting..."
        ).encode('utf-8')
        
        print(f"🚀 PORT_BINDER: Bound to 0.0.0.0:{PORT} in 0.01s")
        sys.stdout.flush()
        
        # Fast response handling
        while True:
            conn, _ = s.accept()
            try:
                # Send pre-generated response immediately
                conn.send(response)
            except OSError as e:
                # Ignore common connection errors
                if e.errno != 32:  # Ignore broken pipe
                    print(f"PORT_BINDER_WARNING: {str(e)}")
            finally:
                try:
                    conn.close()
                except:
                    pass
    except Exception as e:
        print(f"PORT_BINDER_CRITICAL: {str(e)}")
        sys.stdout.flush()
        # Attempt restart after 1 second
        threading.Timer(1.0, bind_port_immediately).start()

# Start binding in a separate thread immediately
threading.Thread(target=bind_port_immediately, daemon=True).start()
