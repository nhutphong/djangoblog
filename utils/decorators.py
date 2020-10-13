from functools import wraps

def record_terminal(name=None, letter='#'):

    def function(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            
            print(f"{name+ ' START ':{letter}^85}")
            fun = func(*args, **kwargs)
            print(f"{name+ ' END ':{letter}^85}", end='\n'*2)
            return fun

        return wrapper
        
        
    return function