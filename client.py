import socket, json, re

bufferSize = 1024 * 100

class Client():
    response = None
    responseTypes = {"io.stream": [], "json": []}

    def connect(self, ip, port):
        self.socketConnection.connect((ip, port))
        return self

    def __init__(self):
        self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def callRoutine(self, routine, call, **args):
        cache = ""
        self.socketConnection.sendall(bytes(json.dumps({"routine": routine, "function": call, "arguments": args}), 'ascii'))
        response = self.socketConnection.recv(bufferSize)

        r = response.decode('utf-8')
        # TODO: Count '{'' & '}', exclude escaped ones - should equal each other - If not, continue because theres more data
        meta = json.loads(r)
        self.header = meta

        if meta.get('type') == 'io.stream':
            f = open('proof-of-working.jpg', 'wb')

        response = self.socketConnection.recv(bufferSize)
        print(response)
        totalBytes = 0
        while(response):
            responseBytes = len(response)

            totalBytes += responseBytes

            if meta.get('type') == 'io.stream':
                print("Wrote %d (%d total) bytes" % (responseBytes, totalBytes))
                f.write(response)
            else:
                print(response)
                cache += response.decode('utf-8')

            if meta.get('type') == 'io.stream' and totalBytes >= meta.get('bytes'):
                break

            response = self.socketConnection.recv(bufferSize)
            print(response)

        if meta.get('type') == 'io.stream':
            f.close()

        if(len(cache) > 0):
            self.response = json.loads(cache)
        return self

    def getResponse(self):
        return self.response

    def getHeader(self):
        return self.header

    def close(self):
        self.socketConnection.close()
        return self