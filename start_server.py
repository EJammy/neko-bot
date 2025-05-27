import socket
import time
import hmac
import config

def wake_server() -> str|None:
    """
    returns error message on error, else returns None
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(5)
        print(f'connecting to {(config.HOST, config.WOL_PORT)}')
        s.connect((config.HOST, config.WOL_PORT))

        def send_recv(data: bytes):
            i = 10
            while i > 0:
                i -= 1
                try:
                    s.sendall(data)
                    ret = s.recv(64)
                except socket.timeout as e:
                    pass
                else:
                    return ret
                print('timeout... retrying')
                time.sleep(1)
            return b''

        print('requesting challenge...')
        challenge = send_recv(b'\x01' + b'\x00' * 7)
        if len(challenge) == 0:
            return 'failed to send receive challenge'
        code = b'\x01\x01' + hmac.digest(config.KEY, challenge, 'sha1')
        print('sending request to wake...' + str(code))
        ret = send_recv(code)
        print(ret)
        if ret != b'\x01\x01\x01\x01':
            return f'error with code: {ret}'

    return None

if __name__ == '__main__':
    wake_server()
