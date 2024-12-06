def function_call_wrapper(func):
    def wrapped(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    wrapped()


def input_result_wrapper(func):
    def wrapped(*args, **kwargs):
        print(f"Calling {func.__name__} with arguments: {args} and {kwargs}.")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returned {result}.")
        return result
    return wrapped
