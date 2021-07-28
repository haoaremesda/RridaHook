import os
import random
import subprocess
import sys
import threading
import time
import traceback

import frida

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import redis as redis
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import win32com.shell.shell as shell

from hook_config import HookIdlefish

idleifsh_ids_key = "idleifsh_ids"
idleifsh_data_key = "idleifsh_data"

RedisHost = "127.0.0.1"
RedisPort = 6379
DatadomeCookieRedisDb = 0
pool = redis.ConnectionPool(host=RedisHost, port=RedisPort, db=DatadomeCookieRedisDb, decode_responses=True)
r = redis.Redis(connection_pool=pool, decode_responses=True)
lock = threading.Lock()


def testing(func):
    def say(*args, **kwargs):
        self = args[0]
        self.kill()
        return func(*args, **kwargs)

    return say


class IdlefishAppiumSpider():
    # 测试开始前执行的方法
    def __init__(self, word, host="127.0.0.1", port=9990):
        self.url = f"http://{host}:{port}/wd/hub"
        self.init_activity = 'com.taobao.fleamarket.home.activity.InitActivity'
        self.main_activity = 'com.taobao.fleamarket.home.activity.MainActivity'
        self.detail_activity = 'com.idlefish.flutterbridge.flutterboost.IdleFishFlutterActivity'
        self.desired_caps = {'platformName': 'Android',  # 平台名称
                             'platformVersion': '11.0',  # 系统版本号
                             'deviceName': '192.168.31.238:5555',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
                             'appPackage': 'com.taobao.idlefish',  # apk的包名
                             # 'appPackage': 'com.qihoo.contents',  # apk的包名
                             'appActivity': self.init_activity,  # activity 名称
                             'noReset': "True",
                             'automationName': 'uiautomator2',
                             'newCommandTimeout': 30000,
                             'disableAndroidWatchers': True,
                             'skipDeviceInitialization': True,
                             'unicodeKeyboard': True,
                             'resetKeyboard': True,
                             'udid': '192.168.31.238:5555',
                             'systemPort': 19990
                             }
        self.front_view_id = "com.taobao.idlefish:id/front_view"
        self.flutter_activity = "com.idlefish.flutterbridge.flutterboost.IdleFishFlutterActivity"
        self.search_but_xpath = "//*[@text='搜索']"
        self.word = word
        self.host = host
        self.port = port
        # self.start_appium()
        self.r = redis.Redis(connection_pool=pool, decode_responses=True)

    def start_driver(self):
        while True:
            try:
                # self.start_mitmp()
                # self.driver = webdriver.Remote(self.url, self.desired_caps)  # 连接Appium
                self.driver = webdriver.Remote(self.url, self.desired_caps)
                self.driver.wait_activity(self.main_activity, 10, 1)
                if self.start_hook():
                    return True
                else:
                    self.kill()
            except BaseException:
                traceback.print_exc()

    def click_front_view(self):
        try:
            front_view = self.driver.find_element_by_id(self.front_view_id)
            front_view.click()
            self.driver.wait_activity(self.flutter_activity, 30, 5)
        except BaseException:
            traceback.print_exc()

    @testing
    def set_word(self, word):
        while True:
            try:
                # edit_text = self.driver.find_element_by_class_name("android.widget.EditText")
                if self.is_element_exist('class="android.widget.EditText"'):
                    edit_text = self.driver.find_element_by_class_name("android.widget.EditText")
                    # edit_text = self.driver.find_element_by_android_uiautomator("text()")
                    if word in edit_text.text:
                        self.driver.implicitly_wait(10)
                        self.driver.find_element_by_xpath(self.search_but_xpath).click()
                        return True
                    elif self.is_element_exist('"粘贴" class="android.widget.Button"') or self.is_element_exist(
                            '"android.widget.Button" text="粘贴"'):
                        self.driver.find_element_by_xpath("//android.widget.Button[@text='粘贴']").click()
                    else:
                        while True:
                            edit_text.clear()
                            if ", " in edit_text.text:
                                continue
                            else:
                                break
                        self.driver.set_clipboard_text(word)
                        TouchAction(self.driver).long_press(edit_text).wait(3000).perform()
                        # edit_text.send_keys(word)
                elif self.is_element_exist(f'text="{self.word}" class="android.view.View"'):
                    return True
                else:
                    self.kill()
                    continue
            except BaseException:
                traceback.print_exc()

    # @testing
    @testing
    def search(self, word):
        while True:
            try:
                # if self.driver.find_element_by_xpath("//android.view.View[contains(@text,'搜索')]"):
                if self.is_element_exist(self.front_view_id):
                    self.click_front_view()
                elif self.is_element_exist('"搜索" class="android.view.View"') or self.is_element_exist(
                        '"android.view.View" text="搜索"'):
                    self.set_word(word)
                # elif self.driver.find_elements_by_xpath("//*[contains(@text,'人想要')]"):
                elif self.is_element_exist('"最新发布"') or self.is_element_exist('已折叠, 综合'):
                    # if self.driver.find_elements_by_xpath("//*[contains(@text,'没有找到你想要的')]"):
                    if self.is_element_exist('小闲鱼没有找到你想要的宝贝'):
                        self.driver.implicitly_wait(5)
                        self.driver.find_element_by_xpath("//*[@text='返回']").click()
                        continue
                    return True
                elif self.is_element_exist("坐下来喝口水"):
                    self.swipe_verify()
                    # return False
                    pass
                elif self.is_element_exist("检查你的网络设置或刷新试试吧") or self.is_element_exist(
                        "无法连接网络") or self.is_element_exist('"我想要" class="android.view.View"'):
                    self.driver.find_element_by_xpath("//android.view.View[@text='返回']").click()
                else:
                    self.kill()
                time.sleep(1)
            except BaseException:
                traceback.print_exc()

    def refresh(self):
        num = 1
        max_num = random.randint(10, 15)
        while True:
            try:
                if self.is_element_exist('已折叠, 最新发布') or self.is_element_exist('已折叠, 综合'):
                    self.driver.implicitly_wait(10)
                    self.driver.find_element_by_xpath("//*[@text='已折叠, 综合']|//*[@text='已折叠, 最新发布']").click()
                # if self.driver.find_element_by_xpath("//*[@text='最新发布']"):
                if self.is_element_exist('"最新发布"'):
                    if num >= max_num:
                        self.driver.close_app()
                        time.sleep(random.randint(80, 180))
                        self.driver.launch_app()
                        self.driver.wait_activity(self.main_activity, 10, 1)
                        self.start_hook()
                        num = 1
                        self.search(self.word)
                    else:
                        self.driver.implicitly_wait(10)
                        self.driver.find_element_by_xpath("//*[@text='最新发布']").click()
                        self.goto_detail()
                        num += 1
                elif self.is_element_exist("坐下来喝口水"):
                    print(f"次数：{num}")
                    self.swipe_verify()
                    # return False
                elif self.is_element_exist("检查你的网络设置或刷新试试吧"):
                    self.driver.find_element_by_xpath("//android.view.View[@text='返回']").click()
                    self.search(self.word)
                else:
                    self.kill()
                time.sleep(random.randint(120, 180))
            except BaseException:
                traceback.print_exc()
            # time.sleep(random.uniform(2, 6))

    def swipe_verify(self):
        try:
            time.sleep(120)
            self.driver.close_app()
            time.sleep(random.randint(80, 180))
            self.driver.launch_app()
            self.start_hook()
        except BaseException:
            traceback.print_exc()
            pass

    # 测试结束后执行的方法
    def tearDown(self):
        try:
            self.driver.quit()
        except Exception:
            pass

    def kill(self):
        while True:
            try:
                if self.is_element_exist("无响应"):
                    self.start_driver()
                elif self.is_element_exist("已停止运行"):
                    self.driver.implicitly_wait(5)
                    self.driver.find_element_by_xpath("//android.widget.Button[@text='确定']").click()
                    self.driver.close_app()
                else:
                    break
            except BaseException:
                traceback.print_exc()
                pass

    def is_element_exist(self, element):
        source = self.driver.page_source
        if element in source:
            return True
        else:
            return False

    def goto_detail(self):
        while True:
            lock.acquire()
            try:
                ids = r.spop(idleifsh_ids_key)
                if not ids:
                    time.sleep(5)
                    continue
            except:
                traceback.print_exc()
                continue
            finally:
                lock.release()
            url = f"https://market.m.taobao.com/app/idleFish-F2e/widle-taobao-rax/page-detail?wh_weex=true&wx_navbar_transparent=true&id={ids}"
            self.goto_good_details(url)
            time.sleep(0.5)

    def goto_good_details(self, url):
        while True:
            try:
                if self.is_element_exist("快速打开复制的网址"):
                    self.driver.find_element_by_xpath("//android.widget.TextView[@text='打开']").click()
                    num = 10
                    while num:
                        if self.is_element_exist("页面尝试打开外部程序"):
                            self.driver.find_element_by_xpath("//android.widget.Button[@text='打开']").click()
                            self.driver.wait_activity(self.detail_activity, 10, 1)
                        elif self.driver.current_activity == self.detail_activity and self.is_element_exist('"android.view.View" text="我想要"'):
                            break
                        time.sleep(1)
                        num -= 1
                else:
                    self.driver.set_clipboard_text(url)
                    self.driver.start_activity("com.ijinshan.browser_fast",
                                               "com.ijinshan.browser.screen.BrowserActivity")
                    self.driver.wait_activity("com.ijinshan.browser.screen.BrowserActivity", 10, 1)
            except BaseException:
                traceback.print_exc()

    # def start_hook(self):
    #     hook_object = HookIdlefish()
    #     return hook_object.start_hook()

    def start_hook(self):
        while True:
            script_js = """
            Java.perform(function () {
            var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
            SwitchConfig.zJ.overload().implementation = function () {
                return false;
            }})
            """
            try:
                str_host = '192.168.31.238:6666'
                manager = frida.get_device_manager()
                remote_device = manager.add_remote_device(str_host)
                session = remote_device.attach("com.taobao.idlefish")
                script = session.create_script(script_js)
                script.load()  # 加载脚本
                return True
            except BaseException:
                traceback.print_exc()

    def start_mitmp(self):
        popens = subprocess.Popen(['mitmdump', '-p', f'{self.port + 1}', '-s',
                                   f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/main_appium/mitmp_idlefish.py'],
                                  stdin=subprocess.PIPE, stderr=sys.stderr, close_fds=True,
                                  stdout=sys.stdout, universal_newlines=True, shell=True, bufsize=1)
        print(f"start_mitmp：{popens.pid}")

    def start_appium(self):
        # commands = f'appium -a 127.0.0.1 -p {self.port} --session-override'
        commands = f'appium -a 127.0.0.1 -p {self.port}'
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c ' + commands)
        # popens = subprocess.Popen(['cmd.exe','appium', '-a', self.host, '-p', str(self.port), '--session-override'],
        #                           stdin=subprocess.PIPE, stderr=sys.stderr, close_fds=True,
        #                           stdout=sys.stdout, universal_newlines=True, shell=True, bufsize=1)
        # print(f"start_appium：{popens.pid}")

    def generate_tracks(self, S):
        """
        :param S: 缺口距离Px
        :return:
        """
        S += 20
        v = 0
        t = 0.2
        forward_tracks = []
        current = 0
        mid = S * 3 / 5  # 减速阀值
        while current < S:
            if current < mid:
                a = 2  # 加速度为+2
            else:
                a = -3  # 加速度-3
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))

        return forward_tracks


if __name__ == '__main__':
    spider = IdlefishAppiumSpider("手机")
    if spider.start_driver():
        print(1)
        spider.goto_detail()
        # if spider.search(spider.word):
        #     print(2)
        #     spider.refresh()
        #     print(4)
    print(spider.driver.get_window_size())
