import os
import sys

import frida

from flask import Flask, jsonify, request


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

basedir = os.path.dirname(__file__)
upload_path = os.path.join(basedir, "test_02.js")
js = open(upload_path, 'r', encoding='utf8').read()
# session = frida.get_usb_device().attach('me.ele')

# session = frida.get_usb_device().attach('com.taobao.idlefish')
# script = session.create_script(js)
# script.on('message', on_message)
# script.load()

process = frida.get_usb_device()
pid = process.spawn(['com.taobao.idlefish'])
# session = process.attach('com.taobao.idlefish')
session = process.attach(pid)
script = session.create_script(js)
script.on('message', on_message)  # 加载回调函数，也就是js中执行send函数规定要执行的python函数
script.load()  # 加载脚本
process.resume(pid)  # 重启app
# sys.stdin.read()

app = Flask(__name__)


@app.route('/test')
def hello_world():
    args = request.args['url_path']
    res = script.exports.callsecretfunctionedy(args)
    return jsonify(res)


@app.route('/result')
def dy_test():
    # url = request.args['url'] #
    res = script.exports.callsecretfunctioneleme()
    print(type(res))
    result = {"status": 200, "data": res}
    return result


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8889, debug=True)