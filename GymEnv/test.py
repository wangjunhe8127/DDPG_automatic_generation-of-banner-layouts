a = [1.1,2.5,3,4,5,6]
def t(b):
    global a
    a = b
def y():
    print(a)
t(6)
y()