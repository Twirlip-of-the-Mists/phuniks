#!/usr/bin/python3

def pairwise(iterable):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        a = iter(iterable)
        return zip(a, a)
    
commands = {}

def __str__(self):
    cmnd_list = []
    for cmnd, functions in commands.items():
        cmnd_list.append(cmnd)
    return f'Commanding({cmnd_list})'
    
def single_on_command(cmnd, function):
    if cmnd not in commands:
        commands[cmnd] = set()
    commands[cmnd].add(function)

def on_command(*args, **kwargs):
    for cmnd, function in pairwise(args):
        single_on_command(cmnd, function)
    for cmnd, function in kwargs.items():
        single_on_command(cmnd, function)

def command(cmnd, *args, **kwargs):
    try:
        functions = commands[cmnd]
    except KeyError:
        print('Command not handled:', cmnd, *args, **kwargs)
    else:
        for function in functions:
            function(cmnd, *args, **kwargs)

def main():
    def cb(name, *args, **kwargs):
        print('cb3', name, *args, **kwargs)
        
    on_command('zoom', cb)
    command('zoom', 'Freddy', 1, [2, 3, 4])
    command('Zoom', 'Freddy', 1, [2, 3, 4])

    return
    
if __name__ == '__main__':
    main()

