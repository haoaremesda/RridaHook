from functools import wraps

from hook_config import HookIdlefish


def funA(func):
    def with_logging(*args, **kwargs):
        print("C语言中文网")
        print("http://c.biancheng.net")
        print(func.__name__ + " was called")
        print(*args, **kwargs)
        return func(*args, **kwargs)
    return with_logging

@funA
def funB(x, z):
    print("学习 Python")
    return True

# z = funB(1111, 44243)
# print(z)

hook_object = HookIdlefish()
hook_object.start_hook()
print("dsadsadsad")
