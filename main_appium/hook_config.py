import traceback

import frida


class HookIdlefish:
    def __init__(self):
        self.script_js = """
        Java.perform(function () {
        var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
        SwitchConfig.zJ.overload().implementation = function () {
            return false;
        }})
        """
        self.app_package = 'com.taobao.idlefish'

    def start_hook(self):
        while True:
            # 管道操作有时较慢，进程还未启动就进行了hook导致frida报错。所以用死循环等待它。
            try:
                process = frida.get_usb_device()
                # pid = process.spawn(['com.taobao.idlefish'])
                session = process.attach(self.app_package)
                # session = process.attach(pid)
                script = session.create_script(self.script_js)
                script.on('message', self.on_message)  # 加载回调函数，也就是js中执行send函数规定要执行的python函数
                script.load()  # 加载脚本
                # process.resume(pid)  # 重启app
                return True
            except frida.ProcessNotFoundError:
                traceback.print_exc()
            except frida.TransportError:
                return False

    def on_message(self, message, data):
        if message['type'] == 'send':
            print("[*] {0}".format(message['payload']))
        else:
            print(message)
