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
        ret = self.db.search("select * from users")
        print(ret)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                print("recv", recv_data.decode('utf-8'), "from", data.addr)
                data.inb += recv_data
            else:
                print("closing connection to", data.addr)
                self.db.sign_out(data.addr)
                self.sel.unregister(sock)
                sock.close()


if __name__ == "__main__":
    server = Server()
    server.main()