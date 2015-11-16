import socket

OOB_PORT = 7778


def setface(device_type):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", OOB_PORT))
    try:
        sock.sendall(bytes("__face__ %s" % device_type, 'ascii'))
    finally:
        sock.close()
