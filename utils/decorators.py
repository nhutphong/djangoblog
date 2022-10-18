from functools import wraps

def record_terminal(name=None, *, char='#'):

    def function(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            
            print(f"{name+ ' START ':{char}^75}")
            fun = func(*args, **kwargs)
            print(f"{name+ ' END ':{char}^75}", end='\n'*2)
            return fun

        return wrapper
        
    return function