num = [0]
def eval_counter(original_function):
    def wrapper(*args, **kwargs):
        num[0] += 1


        if original_function.__name__=="print_eval_num":
            print("Eval_count = ", num[0]-1,'\n')
        return original_function(*args, **kwargs)
    return wrapper

def eval_getter():
    return num[0]