import datetime
import io
import json
import socket
import selectors
import time
import types
import threading

from object.message import Message

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

    def __init__(self, chat_window, server_host="127.0.0.1", server_port=50000):
        self.chat_window = chat_window
        self._server_host = server_host
        self._server_port = server_port
        self.socket = None
        self.t = None
        self._start_connections()

    def _start_connections(self):
        server_addr = (self._server_host, self._server_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(server_addr)
        self.t = threading.Thread(target=self.read_from_server, daemon=True)
        self.t.start()

    def read_from_server(self):
        while True:
            recv = self.socket.recv(2048)
            self._process_recv(recv)
            time.sleep(0.5)

    def _process_recv(self, recv_data):
        try:
            print("recv", repr(recv_data))
            data_dict = self._json_decode(recv_data)
            if recv_data is not None:
                action = data_dict.get("action")
                if action == "transmit":
                    value = data_dict.get("value")
                    from_id = data_dict.get("from_id")
                    print("recv: {} from {}".format(value, from_id))
                    browser_msg = "({} from {}): {}".format(datetime.datetime.now(), from_id, value).rstrip()
                    self.chat_window.textBrowser.append(browser_msg + "\n")
                    self.chat_window.chat_record.append(browser_msg)
                elif action == "file":
                    self.socket.send("ready".encode())
                    self._recv_file(data_dict)
                elif action == "login":
                    login_id = data_dict.get("from_id")
                    self.chat_window.listWidget.addItem(login_id)
                elif action == "out":
                    out_id = data_dict.get("from_id")
                    for i in range(self.chat_window.listWidget.count()):
                        if out_id == self.chat_window.listWidget.item(i).text():
                            self.chat_window.listWidget.takeItem(i)
                            break
                else:
                    print(f'Error: invalid action "{action}".')
        except Exception as e:
            print(e)

    def _recv_file(self, data_dict):
        file_size = data_dict.get("value")
        file_name = data_dict.get("other")
        from_id = data_dict.get("from_id")
        to_id = data_dict.get("to_id")
        recive_size = 0
        res = b""
        while recive_size < file_size:
            data = self.socket.recv(2048)
            recive_size += len(data)
            res += data
        new_file_name = "./recv_file/"+file_name
        f = open(new_file_name, "wb")
        f.write(res)
        f.close()
        browser_msg = "({} from {}): 接收{} 文件成功,保存位置为 {}".format(
            datetime.datetime.now(), from_id, file_name, new_file_name
        ).rstrip()
        self.chat_window.textBrowser.append(browser_msg + "\n")
        self.chat_window.chat_record.append(browser_msg)
        self.socket.send(Message("transmit", to_id, from_id, "{} 文件已收到".format(file_name)).content_bytes)

    def _json_decode(self, json_bytes, encoding="utf-8"):
        try:
            tiow = io.TextIOWrapper(
                io.BytesIO(json_bytes), encoding=encoding, newline=""
            )
            obj = json.load(tiow)
            tiow.close()
            return obj
        except Exception as e:
            print(e)
            return

    def sign_out(self):
        self.socket.close()
