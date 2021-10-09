# -*- coding: utf-8 -*-

import socket


class Network(object):

    def get_available_port(self, port=5531):
        for i in range(20):
            if not self.__is_port_open(port=port + i):
                return port + i

    def get_local_ip(self):
        try:
            localIP = socket.gethostbyname(socket.gethostname())
        except:
            try:
                csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                csock.connect(('8.8.8.8', 80))
                (localIP, port) = csock.getsockname()
                csock.close()
            except socket.error:
                localIP = "127.0.0.1"
        return localIP

    def __is_port_open(self, ip='127.0.0.1', port=5531):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            print(('%d is open' % port))
            return True
        except:
            print(('%d is down' % port))
            return False


network = Network()