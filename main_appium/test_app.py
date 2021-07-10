import random
import time
import traceback

from appium import webdriver


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
                             'deviceName': '127.0.0.1:7555',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
                             'appPackage': 'com.taobao.idlefish',  # apk的包名
                             'appActivity': 'com.taobao.fleamarket.home.activity.InitActivity',  # activity 名称
                             "noReset": "True",
                             'newCommandTimeout': 600,
                             'disableAndroidWatchers': True,
                             'skipDeviceInitialization': True,
                             "unicodeKeyboard": True,
                             "resetKeyboard": True
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
                    while True:
                        edit_text.clear()
                        if ", " in edit_text.text:
                            continue
                        else:
                            break
                    edit_text.send_keys(word)
                    if word in edit_text.text:
                        self.driver.find_element_by_xpath(self.search_but_xpath).click()
                        self.driver.implicitly_wait(10)
                        return True
                else:
                    continue
            except BaseException:
                traceback.print_exc()

    @testing
    def search(self, word):
        self.click_front_view()
        while True:
            try:
                # if self.driver.find_elements_by_xpath("//android.view.View[contains(@text,'搜索')]"):
                if self.is_element_exist('"搜索" class="android.view.View"'):
                    self.set_word(word)
                # elif self.driver.find_elements_by_xpath("//*[contains(@text,'人想要')]"):
                elif self.is_element_exist('人想要" class="android.view.View"'):
                    # if self.driver.find_elements_by_xpath("//*[contains(@text,'没有找到你想要的')]"):
                    if self.is_element_exist('小闲鱼没有找到你想要的宝贝'):
                        self.driver.find_element_by_xpath("//*[@text='返回']").click()
                        self.driver.implicitly_wait(5)
                        continue
                    return True
                else:
                    pass
            except BaseException:
                traceback.print_exc()

    def click_sort(self):
        try:
            self.driver.find_element_by_xpath("//*[@text='已折叠, 综合']|//*[@text='已折叠, 最新发布']").click()
            self.driver.implicitly_wait(10)
        except BaseException:
            traceback.print_exc()

    def refresh(self):
        num = 1
        while True:
            try:
                self.click_sort()
                # if self.driver.find_element_by_xpath("//*[@text='最新发布']"):
                if self.is_element_exist('"最新发布" class="android.view.View"'):
                    self.driver.find_element_by_xpath("//*[@text='最新发布']").click()
                    self.driver.implicitly_wait(10)
                    num += 1
                elif self.is_element_exist("坐下来喝口水"):
                    print(f"次数：{num}")
                    return False
            except BaseException:
                traceback.print_exc()
            time.sleep(random.uniform(2, 6))

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


if __name__ == '__main__':
    tests = MyTests()
    if tests.start_driver():
        print(1)
        if tests.search("手机"):
            print(2)
            tests.refresh()
            print(4)
    print(tests.driver.get_window_size())
