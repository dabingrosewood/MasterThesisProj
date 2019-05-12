num = [0]
def eval_counter(original_function):
    def wrapper(*args, **kwargs):
        num[0] += 1

        # print("执行次数", num[0])
        # only for test

        if original_function.__name__=="print_eval_num":
            print("Eval_count = ", num[0]-1,'\n')
        return original_function(*args, **kwargs)
    return wrapper

# def eval_getter(original_function):
#     def wrapper():
#         return num[0]
#     return wrapper()

def eval_getter():
    return num[0]