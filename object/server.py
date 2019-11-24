import io
import json
import socket
import selectors
import time
import types

from mysql.connectMysql import ConnetMysql
from object.message import Message

class Server():

    def __init__(self, host='127.0.0.1', port=50000):
        self.host = host
        self.port = port
        self.sel = selectors.DefaultSelector()
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id_to_sock = dict()
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
            self.id_to_sock[id[0][0]] = conn
            self._send_login_message_to_other_clients(id[0][0])

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(2048)  # Should be ready to read
            if recv_data:
                self._process_recv(recv_data, data)
            else:
                self._process_client_sign_out(sock, data)

    def _json_decode(self, json_bytes, encoding="utf-8"):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _process_recv(self, recv_data, data):
        try:
            print("recv", repr(recv_data), "from", data.addr)
            data_dict = self._json_decode(recv_data)
            if recv_data is not None:
                action = data_dict.get("action")
                if action == "transmit":
                    to_id = data_dict.get("to_id")
                    sock = self.id_to_sock.get(to_id)
                    sock.send(recv_data)
                    print("send successfully")
                elif action == "file":
                    self._trainsmit_file(recv_data, data_dict)
                elif action == "login" or action == "out":
                    pass
                else:
                    print(f'Error: invalid action "{action}".')
        except Exception as e:
            print(e)

    def _send_login_message_to_other_clients(self, id):
        message = Message("login", id, "", "").content_bytes
        for i in self.id_to_sock.keys():
            if i != id:
                self.id_to_sock[i].send(message)

    def _process_client_sign_out(self, sock, data):
        print("closing connection to", data.addr)
        id = self.db.sign_out(data.addr)
        self.id_to_sock.pop(id)
        self.sel.unregister(sock)
        sock.close()
        for i in self.id_to_sock.keys():
            self.id_to_sock[i].send(Message("out", id, "", "").content_bytes)

    def _trainsmit_file(self, recv_data, data_dict):
        to_id = data_dict.get("to_id")
        from_id = data_dict.get("from_id")
        from_sock = self.id_to_sock.get(from_id)
        sock = self.id_to_sock.get(to_id)
        file_size = data_dict.get("value")
        sock.send(recv_data)
        time.sleep(0.5)
        ready_msg = sock.recv(2048)
        if ready_msg.decode() == "ready":
            total_recv = 0
            res = b""
            while total_recv < file_size:
                file_data = from_sock.recv(2048)
                res += file_data
                total_recv += len(file_data)
            sock.sendall(res)
            time.sleep(0.5)

if __name__ == "__main__":
    server = Server()
    server.main()