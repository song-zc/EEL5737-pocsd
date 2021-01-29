from xmlrpc.server import SimpleXMLRPCServer

# A marshalling error is going to occur because we're returning a
# complex number
def add(x, y):
    return x+y

server = SimpleXMLRPCServer(('127.0.0.1', 8000))
print("Listening on port 8000...")
server.register_function(add, 'add')

server.serve_forever()