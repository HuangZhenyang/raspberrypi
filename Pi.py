#!/usr/bin/env python
#  -*-coding:utf-8 -*-

__author__ = 'Huang Zhenyang'
__version__ = '1.0.1'
__email__ = '745125931@qq.com'

#  ----Import----
import socket
import os
#  ----EndImport----


class Pi(object):

    def __init__(self):
        # socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.BUFSIZE = 1024
        self.HOST = 'localhost'  # 0.0.0.0
        self.PORT = 8001
        self.server.bind((self.HOST, self.PORT))

        '''
        # camera parameters
        self.ex = ['auto', 'night', 'nightpreview', 'backlight', 'spotlight', 'sports', 'snow', 'beach', 'verylong',
                   'fixedfps', 'antishake', 'fireworks']
        self.awb = ['auto', 'off', 'sun', 'cloud', 'shade', 'tungsten', 'fluorescent', 'incandescent', 'flash',
                    'horizon']
        self.ifx = ['none', 'negative', 'solarise', 'posterize', 'whiteboard', 'blackboard', 'sketch', 'denoise',
                    'emboss', 'oilpaint', 'hatch', 'gpen', 'pastel', 'watercolour', 'film', 'blur', 'saturation']
        '''

    def connecttouser(self):
        self.server.listen(5)
        print 'wait for user'
        try:
            while True:
                client, addr = self.server.accept()
                client.settimeout(10*1000)
                print 'get connection from ', addr
                while True:
                    data = client.recv(self.BUFSIZE)
                    print 'from user:', data
                    data = data.split("_")
                    i = 0
                    if data[0] == 'take photos':
                        command = "raspistill "

                        if data[1] == '-t 0':
                            command += "-o image.jpg "
                            for i in range(2, len(data)):
                                command = command + data[i] + " "
                        else:
                            command = command + data[1] + "-o image.jpg "
                            for i in range(2, len(data)):
                                command = command + data[i] + " "

                        # command = "raspostill image%s.jpg " % i + " ".join([x for x in list(data[1:]) if x != "-t 0"])

                        print command

                        #  os.system(command)
                        os.system("ping www.baidu.com")
                        print 'Done'
                        i += 1
                    elif data == 'quit' or data == ' ':
                        break
                client.close()
            self.server.close()
        except socket.error:
            print 'shutdown'


if __name__ == '__main__':
    pi = Pi()
    pi.connecttouser()







