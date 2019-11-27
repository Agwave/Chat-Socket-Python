import datetime
import io
import json
import socket
import time
import threading

from object.message import Message


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
        try:
            while True:
                recv = self.socket.recv(2048)
                self._process_recv(recv)
                time.sleep(0.5)
        except Exception as e:
            print(e)
            self.sign_out()

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
