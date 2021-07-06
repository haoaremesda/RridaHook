import os
import sys

import frida

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

basedir = os.path.dirname(__file__)
upload_path = os.path.join(basedir, "test_01.js")
js = open(upload_path, 'r', encoding='utf8').read()

# session = frida.get_usb_device().attach('me.ele')
# session = frida.get_usb_device().attach('com.taobao.idlefish')
process = frida.get_usb_device()
pid = process.spawn(['com.taobao.idlefish'])
# session = process.attach('com.taobao.idlefish')
session = process.attach(pid)
script = session.create_script(js)
script.on('message',on_message) #加载回调函数，也就是js中执行send函数规定要执行的python函数
script.load() #加载脚本
process.resume(pid)  # 重启app
sys.stdin.read()