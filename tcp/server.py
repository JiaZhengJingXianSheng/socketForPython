# !/usr/bin/python3
# -*- coding:utf-8 -*-
import socket
import select


def main():

    serverIp = ''
    serverPort = 2101

    tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSock.bind((serverIp, serverPort))
    tcpSock.listen(5)
    print('Port ' + str(serverPort) + ' is listening')
    inputs = [tcpSock]

    while True:
        rs, ws, es = select.select(inputs, [], [])

        for r in rs:
            if r is tcpSock:
                cli, addr = tcpSock.accept()

                connInfo = 'User ' + str(addr) + ' is connected'
                print(connInfo)
                inputs.append(cli)
                for sock in inputs:
                    if sock is tcpSock:
                        continue
                    if sock is cli:
                        sock.send('Welcome to server'.encode('utf-8'))
                        continue
                    sock.send(connInfo.encode('utf-8'))

            else:
                try:
                    data = r.recv(1024)
                    disconnected = not data
                except socket.error:
                    disconnected = True
                                    
                if disconnected:
                    disconnInfo = 'User ' + \
                        str(r.getpeername()) + 'is disconnected'
                    print(disconnInfo)
                    inputs.remove(r)
                    for sock in inputs:
                        if sock is tcpSock:
                            continue
                        sock.send(disconnInfo.encode('utf-8'))

                else:
                    try:
                        recvInfo = str(r.getpeername()) + \
                            ': ' + data.decode('utf-8')
                    except UnicodeDecodeError as err:
                        print("Unicode Decode Error {0}".format(err))
                    except:
                        raise

                    print(recvInfo)
                    for sock in inputs:
                        if sock is tcpSock:
                            continue
                        sock.send(recvInfo.encode('utf-8'))


if __name__ == '__main__':
    main()
