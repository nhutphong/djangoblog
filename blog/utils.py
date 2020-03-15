

def design(name=None, letter='#'):
    def function(func):
        def wrapped(*args, **kwargs):
            print(f"{name:{letter}^90}")
            func(*args, **kwargs)
            print(f"{name:{letter}^90}", end='\n'*2)
        return wrapped
    return function