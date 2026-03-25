import socket
import json
import threading
import time

class BluetoothSender:
    def __init__(self, mode="server", target_mac=None, port=1):
        """
        Initialize Bluetooth Sender.
        
        :param mode: "server" (laptop listens for phone to connect) or "client" (laptop connects to phone)
        :param target_mac: MAC address of the phone (only required if mode="client")
        :param port: RFCOMM port (usually 1)
        """
        self.mode = mode
        self.target_mac = target_mac
        self.port = port
        self.sock = None
        self.client_sock = None
        self.connected = False
        self._lock = threading.Lock()

    def start(self):
        """Start the Bluetooth connection process based on the mode."""
        if self.mode == "server":
            # Run server in a background thread so it doesn't block the video stream
            thread = threading.Thread(target=self._start_server, daemon=True)
            thread.start()
        elif self.mode == "client":
            thread = threading.Thread(target=self._start_client, daemon=True)
            thread.start()
            
    def _start_server(self):
        try:
            self.sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            # Explicitly bind to this laptop's Bluetooth MAC instead of ""
            self.sock.bind(("A4:C3:F0:51:C4:B6", self.port))
            self.sock.listen(1)
            print(f"🔵 Bluetooth Server running. Waiting for connection on RFCOMM channel {self.port}...")
            
            # This blocks until a connection is made
            self.client_sock, client_info = self.sock.accept()
            print(f"✅ Accepted Bluetooth connection from {client_info}")
            with self._lock:
                self.connected = True
                
        except Exception as e:
            print(f"❌ Error starting Bluetooth server: {e}")

    def _start_client(self):
        if not self.target_mac:
            print("❌ Error: target_mac is required for client mode.")
            return

        print(f"🔵 Connecting to {self.target_mac} on port {self.port}...")
        
        while not self.connected:
            try:
                self.sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                self.sock.connect((self.target_mac, self.port))
                self.client_sock = self.sock
                with self._lock:
                    self.connected = True
                print(f"✅ Successfully connected to Android device ({self.target_mac})")
            except Exception as e:
                # Silently retry every 2 seconds without cluttering console unless it's a new error
                time.sleep(2)

    def send_data(self, data_dict):
        """
        Sends dictionary data as a JSON string over Bluetooth.
        :param data_dict: Dictionary containing the detection data
        """
        with self._lock:
            if not self.connected or self.client_sock is None:
                return False
        
        try:
            # Add a newline so the receiver can easily read line-by-line
            message = json.dumps(data_dict) + "\n"
            self.client_sock.send(message.encode('utf-8'))
            return True
        except Exception as e:
            print(f"⚠️ Bluetooth send error: {e}")
            with self._lock:
                self.connected = False
                if self.client_sock:
                    self.client_sock.close()
                self.client_sock = None
            
            # If we were acting as a server, wait for a new connection
            if self.mode == "server":
                print("🔵 Bluetooth connection lost. Restarting server...")
                self.start()
            elif self.mode == "client":
                print("🔵 Bluetooth connection lost. Attempting to reconnect...")
                self.start()
            return False

    def close(self):
        """Closes the Bluetooth sockets cleanly."""
        with self._lock:
            self.connected = False
            if self.client_sock:
                try:
                    self.client_sock.close()
                except:
                    pass
            if self.sock and self.mode == "server":
                try:
                    self.sock.close()
                except:
                    pass
