from socket import *
from select import *


class HttpServer():
    def __init__(self, host, port, dir):
        self.host = host
        self.port = port
        self.dir = dir
        self.address = (host, port)
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.socketfd = socket()
        self.socketfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def bind(self):
        self.socketfd.bind(self.address)

    def serve_forever(self):
        self.socketfd.listen(5)
        print('Listen to port %d' % self.port)
        self.rlist.append(self.socketfd)
        while True:
            rl, wl, xl = select(self.rlist, self.wlist, self.xlist)
            for r in rl:
                if r is self.socketfd:
                    confd, addr = r.accept()
                    self.rlist.append(confd)
                else:
                    self.handle(confd)

    def handle(self, confd):
        # 接收请求
        request = confd.recv(4096)
        # 断开链接的处理
        if not request:
            self.rlist.remove(confd)
            confd.close()
            return
            # 提取命令行
        request_line = request.splitlines()[0]
        # 提取访问内容
        info = request_line.decode().split(' ')[1]
        # 打印要访问的内容
        print(confd.getpeername(), ':', info)
        # 对内容进行判定
        if info == '/' or info[-5:] == '.html':
            self.get_html(confd, info)
        else:
            self.get_data(confd, info)

    def get_html(self, confd, info):
        if info == '/':
            filename = self.dir + '/index.html'
        else:
            filename = self.dir + info
        try:
            fd = open(filename)
        except Exception:
            response = '''HTTP/1.1 404 Not Found
                        ContentType: text/html
                        
                        <h1> Sorry....</h1>
            '''
        else:
            response = '''HTTP/1.1 200 Not Found
                         ContentType: text/html

            '''
            response += fd.read()
        finally:
            confd.send(response.encode())

    def get_data(self, confd, info):
        response = '''HTTP/1.1 200 Not Found
                     ContentType: text/html

                     <h1> Waiting for HttpServer 3.0....</h1>
                    '''
        confd.send(response.encode())


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8000
    DIR = './httpserver2.0/static'
    httpfd = HttpServer(HOST, PORT, DIR)
    httpfd.serve_forever()
