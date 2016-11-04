#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Huang Zhenyang'
__version__ = '1.0.1'
__email__ = '745125931@qq.com'

#  ----Import----
import socket
import wx
import re
#  ----EndImport----


class User(object):

    def __init__(self):
        self.BUFSIZE = 1024
        self.HOST = '127.0.0.1'  #  172.18.171.3   172.25.73.2
        self.PORT = 8001
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connecttopi(self):
        try:
            self.client.connect((self.HOST, self.PORT))
            print '>>> Connect to pi'
        except socket.error:
            self.client.close()
            print ">>> Can't connect to pi"

    def sendcommand(self, command):
        try:
            self.client.send(command.encode('utf-8'))
        except socket.error:
            self.client.close()
            print 'shutdown connection'


class MyFrame(wx.Frame):

    def __init__(self, parent, id, user):
        self.user = user

        wx.Frame.__init__(self, parent, id, 'Remote Camera to Raspberry Pi', size=(800, 450))
        self.panel = wx.Panel(self)

        # button
        self.button = wx.Button(self.panel, label=u"拍照", pos=(320, 310), size=(100, 30))

        # slider
        slider_table_font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        slider_table = wx.StaticText(self.panel, -1, u'延时时长(s)：', pos=(550, 30), size=(60, 20))
        slider_table.SetFont(slider_table_font)
        self.slider = wx.Slider(self.panel, -1, 0, 0, 60, pos=(600, 50), size=(50, 250),
                                style=wx.SL_VERTICAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.slider.SetTickFreq(2, 1)

        # ex_choice
        ex_choice_label = wx.StaticText(self.panel, -1, u'曝光模式：', pos=(20, 50), size=(70, 30))
        ex_choice_list = [u'自动曝光模式（默认）', u'夜间拍摄模式', u'夜间预览拍摄模式', u'逆光拍摄模式',
                          u'聚光灯拍摄模式', u'运动拍摄模式', u'雪景优化拍摄模式', u'海滩优化拍摄模式',
                          u'长时间曝光拍摄模式', u'帧约束拍摄模式', u'防抖模式', u'烟火优化拍摄模式', u'']
        self.ex_choice = wx.Choice(self.panel, -1, pos=(100, 45), choices=ex_choice_list)
        self.ex = ['auto', 'night', 'nightpreview', 'backlight', 'spotlight', 'sports', 'snow', 'beach', 'verylong',
                   'fixedfps', 'antishake', 'fireworks', '']

        # awb_choice
        awb_choice_label = wx.StaticText(self.panel, -1, u'自动白平衡：', pos=(20, 80), size=(80, 30))
        awb_choice_list = [u'自动模式（默认）', u'关闭白平衡测算', u'日光模式', u'多云模式', u'阴影模式', u'钨灯模式',
                           u'荧光灯模式', u'白炽灯模式', u'闪光模式', u'地平线模式', u'']
        self.awb_choice = wx.Choice(self.panel, -1, pos=(100, 80), choices=awb_choice_list)
        self.awb = ['auto', 'off', 'sun', 'cloud', 'shade', 'tungsten', 'fluorescent', 'incandescent', 'flash',
                    'horizon', '']

        # ifx_choice
        ifx_choice_label = wx.StaticText(self.panel, -1, u'图像特效：', pos=(20, 120), size=(80, 30))
        ifx_choice_list = [u'无特效（默认）', u'反色图像', u'曝光过度图像', u'色调图像', u'白板特效', u'黑板特效',u'素描风格特效',
                           u'降噪图像', u'浮雕图像', u'油画风格特效', u'草图特效', u'马克笔特效',u'柔化风格特效',
                           u'水彩风格特效', u'胶片颗粒风格特效', u'模糊图像', u'色彩饱和图像', u'']
        self.ifx_choice = wx.Choice(self.panel, -1, pos=(100, 120), choices=ifx_choice_list)
        self.ifx = ['none', 'negative', 'solarise', 'posterize', 'whiteboard', 'blackboard', 'sketch', 'denoise',
                    'emboss', 'oilpaint', 'hatch', 'gpen', 'pastel', 'watercolour', 'film', 'blur',
                    'saturation', '']

        # mm_choice
        mm_choice_label = wx.StaticText(self.panel, -1, u'测光模式：', pos=(20, 160), size=(80, 30))
        mm_choice_list = [u'全画面平衡测光', u'点测光', u'模拟背光图像', u'阵列测光', u'']
        self.mm_choice = wx.Choice(self.panel, -1, pos=(100, 160), choices=mm_choice_list)
        self.mm = ['average', 'spot', 'backlit', 'matrix', '']


        # pictures' width and height
        width_label = wx.StaticText(self.panel, -1, u'照片宽：', pos=(20, 210), size=(50, 30))
        self.width_text = wx.TextCtrl(self.panel, -1, u"64~1920", pos=(70, 210), size=(60, -1))
        self.width_text.SetInsertionPoint(0)

        height_label = wx.StaticText(self.panel, -1, u'照片高：', pos=(140, 210), size=(50, 30))
        self.height_text = wx.TextCtrl(self.panel, -1, u"64~1080", pos=(190, 210), size=(60, -1))
        self.height_text.SetInsertionPoint(0)

        # bind
        self.Bind(wx.EVT_BUTTON, self.takephotos, self.button)
        self.Bind(wx.EVT_CLOSE, self.closewindow)

    def takephotos(self, event):
        #  获取复选框的参数，并以下划线分割方式发送给pi  树莓派那边是用参数组成的列表。
        # 而ex_choice.GetSelection()返回索引

        command = "take photos" + "_-t " + str(self.slider.GetValue() * 1000) + " "
        l = lambda x: x != -1
        if l(self.ex_choice.GetSelection()):
            command += "_-ex " + self.ex[self.ex_choice.GetSelection()]
        if l(self.awb_choice.GetSelection()):
            command += "_-awb " + self.awb[self.awb_choice.GetSelection()]
        if l(self.ifx_choice.GetSelection()):
            command += "_-ifx " + self.ifx[self.ifx_choice.GetSelection()]
        if l(self.mm_choice.GetSelection()):
            command += "_-mm " + self.mm[self.mm_choice.GetSelection()]

        t = lambda x: x.isdigit()
        if t(self.width_text.GetValue()):
            command += "_-w " + self.width_text.GetValue()
        if t(self.height_text.GetValue()):
            command += "_-h" + self.width_text.GetValue()

        self.user.sendcommand(command)

    def closewindow(self, event):
        self.user.sendcommand("quit")
        self.Destroy()


def main():
    user = User()
    user.connecttopi()

    app = wx.PySimpleApp()
    frame = MyFrame(parent=None, id=-1, user=user)
    frame.Show()

    app.MainLoop()


if __name__ == '__main__':
    main()







