import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 1717))
server.listen(4)

def start_server():
    try:
        while True:
            print('waiting for a connection')
            client_socket, address = server.accept()
            print(f'connection succesful with {address}')

            data = client_socket.recv(1024).decode('utf-8')

            HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
            content = 'Lets go...'.encode('utf-8')
            client_socket.send(HDRS.encode('utf-8') + content)
            client_socket.shutdown(socket.SHUT_WR)
            print(f'connection shutdown with {address}')
    except KeyboardInterrupt:
        server.close()
        print('Server shutdown...')
    except:
        pass

if __name__ == '__main__':
    start_server()