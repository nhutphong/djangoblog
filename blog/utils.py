

def design(name=None, letter='#'):
    def function(func):
        def wrapped(*args, **kwargs):
            print(f"{name:{letter}^90} - START")
            fun = func(*args, **kwargs)
            print(f"{name:{letter}^90} - END", end='\n'*2)
            return fun
        return wrapped
    return function