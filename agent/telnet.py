import telnetlib
import select

class TelnetClient:
    def __init__(self, host, port, timeout=10, encoding="ascii"):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.telnet = None
        self.default_encoding = encoding

    def connect(self):
        """Establishes a connection to the Telnet server."""
        try:
            self.telnet = telnetlib.Telnet(self.host, self.port, self.timeout)
            print(f"Connected to {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to connect: {e}")

    def send(self, message):
        """Sends a message to the Telnet server."""
        try:
            if self.telnet:
                self.telnet.write(message.encode(self.default_encoding))
                # print(f"Sent: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive(self):
        """Checks for incoming messages without blocking."""
        try:
            if self.telnet:
                ready, _, _ = select.select([self.telnet], [], [], 0.1)
                if ready:
                    message = self.telnet.read_until(b"\n", timeout=1).decode(self.default_encoding).strip()
                    if message:
                        # print(f"Received: {message}")
                        return message
        except Exception as e:
            print(f"Error receiving message: {e}")
        return None

    def close(self):
        """Closes the Telnet connection."""
        if self.telnet:
            self.telnet.close()
            print("Connection closed.")