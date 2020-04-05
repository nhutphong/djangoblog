

def design(name=None, letter='#'):
    def function(func):
        def wrapped(*args, **kwargs):
            print(f"{name+ ' START ':{letter}^85}")
            fun = func(*args, **kwargs)
            print(f"{name+ ' END ':{letter}^85}", end='\n'*2)
            return fun

        return wrapped
        
    return function