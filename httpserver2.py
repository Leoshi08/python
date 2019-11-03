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
        if info == "/":
            filename = self.dir + "/index.html"
        else:
            filename = self.dir + info
        try:
            fd = open(filename)
        except Exception:
            response = '''HTTP/1.1 404 Not Found
                        Content-Type:text/html
            
                        <h1>Sorry....</h1>
                       '''
        else:
            response = '''HTTP/1.1 200 Not Found
                        Content-Type:text/html

                        '''
            response += fd.read()
        finally:
            confd.send(response.encode())

    def get_data(self, confd, info):
        response = "HTTP/1.1 200 OK\r\n"
        response += 'Content-Type:text/html\r\n'
        response += '\r\n'
        response += "<h1>Waiting for httpserver 3.0</h1>"
        confd.send(response.encode())



# 用户使用HTTPServer
if __name__ == "__main__":
    """
    通过 HTTPServer类快速搭建服务，展示自己的网页
    """
    # 用户决定的参数
    HOST = '0.0.0.0'
    PORT = 8000
    DIR = './static'  # 网页存储位置

    httpd = HttpServer(HOST, PORT, DIR)  # 实例化对象
    httpd.serve_forever()  # 启动服务