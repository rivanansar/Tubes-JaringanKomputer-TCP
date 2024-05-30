import socket   #menyediakan low-level interface untuk sebuah jaringan komunikasi

#untuk membuat socket baru, menunjuk IPv4, serta menunjuk bahwa format ini menggunakan TCP dan untuk direktori client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   

#mengaitkan alamat IP dan port
client_socket.connect(("127.0.0.1", 8080))

#menandakan bahwa sinyal dari server sudah di dapat
http_request = "GET /index.html HTTP/1.1\r\n"
http_request += "Host: 127.0.0.1:8080\r\n"
http_request += "\r\n"

#menerima sinyal http request dari server
client_socket.send(http_request.encode())

#merespon sinyal http request
response = client_socket.recv(4096).decode()

#menerima response dari server
print("Received response from server:")
print(response)

#menutup socket client
client_socket.close()