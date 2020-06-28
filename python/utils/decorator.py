# coding=utf-8


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            return {"result": None, "success": False}
    return inner_function
