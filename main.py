import frida

from flask import Flask, jsonify, request


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


js = open('test_02.js', 'r', encoding='utf8').read()
# session = frida.get_usb_device().attach('me.ele')
session = frida.get_usb_device().attach('com.taobao.idlefish')
script = session.create_script(js)
script.on('message', on_message)
script.load()

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