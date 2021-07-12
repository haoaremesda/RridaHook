import random
import time
import traceback

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def testing(func):
    def say(*args, **kwargs):
        self = args[0]
        self.kill()
        return func(*args, **kwargs)

    return say


class MyTests():
    # 测试开始前执行的方法
    def __init__(self):
        self.url = "http://127.0.0.1:8889/wd/hub"
        self.desired_caps = {'platformName': 'Android',  # 平台名称
                             'platformVersion': '6.0.1',  # 系统版本号
                             'deviceName': 'kkkkkkkkk',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
                             # 'appPackage': 'com.taobao.idlefish',  # apk的包名
                             # 'appActivity': 'com.taobao.fleamarket.home.activity.InitActivity',  # activity 名称
                             'noReset': "True",
                             'newCommandTimeout': 600,
                             'disableAndroidWatchers': True,
                             'skipDeviceInitialization': True,
                             'unicodeKeyboard': True,
                             'resetKeyboard': True,
                             'udid': 'f5c6c341'
                             }
        self.front_view_id = "com.taobao.idlefish:id/front_view"
        self.flutter_activity = "com.idlefish.flutterbridge.flutterboost.IdleFishFlutterActivity"
        self.search_but_xpath = "//*[@text='搜索']"

    def start_driver(self):
        try:
            self.driver = webdriver.Remote(self.url, self.desired_caps)  # 连接Appium
            self.driver.implicitly_wait(10)
        except BaseException:
            traceback.print_exc()
        else:
            return True

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
                    if word in edit_text.text:
                        self.driver.find_element_by_xpath(self.search_but_xpath).click()
                        self.driver.implicitly_wait(10)
                        return True
                    else:
                        while True:
                            edit_text.clear()
                            if ", " in edit_text.text:
                                continue
                            else:
                                break
                        edit_text.send_keys(word)
                else:
                    continue
            except BaseException:
                traceback.print_exc()

    @testing
    def search(self, word):
        self.click_front_view()
        while True:
            try:
                # if self.driver.find_element_by_xpath("//android.view.View[contains(@text,'搜索')]"):
                if self.is_element_exist('"搜索"'):
                    self.set_word(word)
                # elif self.driver.find_elements_by_xpath("//*[contains(@text,'人想要')]"):
                elif self.is_element_exist('人想要"'):
                    # if self.driver.find_elements_by_xpath("//*[contains(@text,'没有找到你想要的')]"):
                    if self.is_element_exist('小闲鱼没有找到你想要的宝贝'):
                        self.driver.find_element_by_xpath("//*[@text='返回']").click()
                        self.driver.implicitly_wait(5)
                        continue
                    return True
                elif self.is_element_exist("坐下来喝口水"):
                    self.swipe_verify()
                else:
                    pass
            except BaseException:
                traceback.print_exc()

    def refresh(self):
        num = 1
        while True:
            try:
                if self.is_element_exist('已折叠, 最新发布') or self.is_element_exist('已折叠, 综合'):
                    self.driver.find_element_by_xpath("//*[@text='已折叠, 综合']|//*[@text='已折叠, 最新发布']").click()
                    self.driver.implicitly_wait(10)
                # if self.driver.find_element_by_xpath("//*[@text='最新发布']"):
                if self.is_element_exist('"最新发布"'):
                    self.driver.find_element_by_xpath("//*[@text='最新发布']").click()
                    self.driver.implicitly_wait(10)
                    num += 1
                elif self.is_element_exist("坐下来喝口水"):
                    print(f"次数：{num}")
                    self.swipe_verify()
                    return False
            except BaseException:
                traceback.print_exc()
            # time.sleep(random.uniform(2, 6))

    def swipe_verify(self):
        try:
            if self.is_element_exist("非常抱歉，这出错了"):
                self.driver.find_element_by_xpath("//*[contains(@text,'刷新')]/..").click()
            if self.is_element_exist("向右滑动验证"):
                k = 0
                start_but = self.driver.find_element_by_xpath("//*[@id='nc_1_n1t']|//*[@resource-id='nc_1_n1t']")
                start_but_rect = start_but.rect
                end_but = self.driver.find_element_by_xpath("//*[contains(@text,'向右滑动验证')]")
                end_but_rect = end_but.rect
                swipe_end = end_but_rect['x'] + end_but_rect['width']
                tracks = self.generate_tracks(swipe_end)
                action = TouchAction(self.driver)
                # action.long_press(start_but, swipe_end, end_but_rect['y'], 3000)
                for s in tracks:
                    k += end_but_rect['x'] + s
                    # self.driver.swipe(start_but_rect['x'] + random.uniform(10, start_but_rect['width']), start_but_rect['y'], k, end_but_rect['y'])
                    action.move_to(start_but)
        except BaseException:
            pass

    # 测试结束后执行的方法
    def tearDown(self):
        try:
            self.driver.quit()
        except Exception:
            pass

    def kill(self):
        try:
            if self.is_element_exist("无响应"):
                self.driver.launch_app()
        except BaseException:
            pass

    def is_element_exist(self, element):
        source = self.driver.page_source
        if element in source:
            return True
        else:
            return False

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
    tests = MyTests()
    if tests.start_driver():
        print(1)
        if tests.search("手机"):
            print(2)
            tests.refresh()
            print(4)
    print(tests.driver.get_window_size())
