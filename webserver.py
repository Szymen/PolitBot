import socket
# configuration
host, port = '0.0.0.0', 5000
server_address = (host, port)
request_queue_size = 1
maximum_request_size = 1024
# create a socket
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(server_address)
listen_socket.listen(request_queue_size)

print 'Serving HTTP on port %s ...' % port
while True:
    client_connection, client_address = listen_socket.accept()
    http_req = client_connection.recv(maximum_request_size)
    print http_req
    
    http_response = """\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)
    client_connection.close()
