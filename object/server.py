import io
import json
import socket
import selectors
import types

from mysql.connectMysql import ConnetMysql


class Server():

    def __init__(self, host='127.0.0.1', port=50000):
        self.host = host
        self.port = port
        self.sel = selectors.DefaultSelector()
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socks = dict()
        self.db = ConnetMysql()
        self.start()


    def start(self):
        self.lsock.bind((self.host, self.port))
        self.lsock.listen()
        print("listening on", (self.host, self.port))
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

    def main(self):
        try:
            while True:
                events = self.sel.select(timeout=None)

                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()


    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print("accepted connection from", addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        self.db.update("update users set ip = %s, port = %s where alive = 1 and ip = '0' and port = 0", addr)
        id = self.db.search("select id from users where ip = %s and port = %s and alive = 1", addr)
        print("id: ", id)
        if id != ():
            self.socks[id[0][0]] = conn

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                print("recv", repr(recv_data), "from", data.addr)
                self.process_recv(recv_data)
            else:
                print("closing connection to", data.addr)
                self.db.sign_out(data.addr)
                self.sel.unregister(sock)
                sock.close()
                
    def _json_decode(self, json_bytes, encoding="utf-8"):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def process_recv(self, data_recv):
        data_dict = self._json_decode(data_recv)
        if data_recv is not None:
            action = data_dict.get("action")
            if action == "transmit":
                to_id = data_dict.get("to_id")
                value = data_dict.get("value")
                sock = self.socks.get(to_id)
                print(sock)
                sock.send(value.encode("utf-8"))
                print("send successfully")
            elif action == "login" or action == "out":
                pass
            else:
                content = {"result": f'Error: invalid action "{action}".'}

if __name__ == "__main__":
    server = Server()
    server.main()