import socket
import selectors
import types
import threading


class ClientSel:

    def __init__(self, server_host="127.0.0.1", server_port=50000):

        self.server_host = server_host
        self.server_port = server_port
        self.sel = selectors.DefaultSelector()
        self.socket = self.start_connections()
        # 还需要有自己的ip和端口号，需要server发送过来

    def start_connections(self):
        server_addr = (self.server_host, self.server_port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ
        data = types.SimpleNamespace(
            inb=b"",
            outb=b"",
        )
        self.sel.register(sock, events, data=data)
        return sock


    def main(self):
        try:
            while True:
                events = self.sel.select(timeout=None)
                if events:
                    for key, mask in events:
                        self.service_connection(key, mask)
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                print("received", repr(recv_data))
                data.inb += recv_data
            if not recv_data:
                print("closing connection")
                self.sel.unregister(sock)
                sock.close()

    def sign_out(self):
        self.socket.close()


class Client(object):

    def __init__(self, server_host="127.0.0.1", server_port=50000):
        self._server_host = server_host
        self._server_port = server_port
        self.socket = None
        self._start_connections()
        # 还需要有自己的ip和端口号，需要server发送过来

    def _start_connections(self):
        server_addr = (self.server_host, self.server_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(server_addr)
        threading.Thread(target=self.read_from_server).start()

    def read_from_server(self):
        while True:
            recv = self.socket.recv(2048).decode("utf-8")
            print(recv)
