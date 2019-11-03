'''
httpserver 2.0
多路复用和httpserver练习,基于python3.5
'''

from socket import *
from select import *


class HttpServer():
    # 建立初始化函数
    def __init__(self, host='0.0.0.0', port=8000, dir=None):
        self.host = host
        self.port = port
        self.dir = dir
        self.address = (host, port)
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()

    # 建立套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def bind(self):
        self.sockfd.bind(self.address)

    def serve_forever(self):
        self.sockfd.listen(5)
        print("Listening to port", self.port)
        self.rlist.append(self.sockfd)
        while True:
            rs, wls, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sockfd:
                    c, addr = r.accept()
                    self.rlist.append(c)
                else:
                    self.handle(c)

    def handle(self, confd):
        # 接收http请求
        request = confd.recv(4096)
        # 客户端断开
        if not request:
            self.rlist.remove(confd)
            confd.close()
            return
            # 提取客户端请求
        request_line = request.splitlines()[0]
        info = request_line.decode().split(' ')[1]
        print(confd.getpeername(), ':', info)

        # 根据请求内容进行数据整理
        # 分为两类 1.请求网页  2.其他
        if info == "/" or info[-5:] == '.html':
            self.get_html(confd, info)
        else:
            self.get_data(confd.info)

    def get_html(self, confd, info):
        pass

    def get_data(self, confd, info):
        pass
