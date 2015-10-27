
def calcula_rpm(a , b):
    A = int(a, 16)
    B = int(b, 16)
    rpm = ((A * 256) + B) / 4
    print rpm
