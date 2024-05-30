import socket   #menyediakan low-level interface untuk sebuah jaringan komunikasi
import os       #menyediakan cara untuk berinteraksi dengan operating system yang bisa melakukan beberapa jenis tugas
import mimetypes    #mengidentifikasi format file spesific di internet

#untuk membuat socket baru, menunjuk IPv4, serta menunjuk bahwa format ini menggunakan TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   

#mengatur alamat IP dan port
IP = "127.0.0.1"
port = 8080

# Mengaitkan socket dengan alamat IP dan port
server_socket.bind((IP, port))

#membuat listening socket untuk menerima koneksi
server_socket.listen(5)

print(f"Web server is running on {IP}:{port}...")  #print

while True:
    client_socket, client_addr = server_socket.accept() #untuk menerima koneksi dari client socket dan client address ke server socket
    request = client_socket.recv(1024).decode() #untuk meminta data client socket
    print(f"Request from {client_addr}: {request}") #print permintaan dari client addr

    request_line = request.split("\r\n")[0] #untuk meminta line pertama dari http request
    method, path, _ = request_line.split(" ")   #untuk memisahkan line http request dengan komponen individu

    #ketika mendapatkan GET maka index.html akan terdapat link
    if method == "GET":
        if path == "/":
            path = "/index.html"

        #untuk mengikuti/menyambukan ke folder wwwroot
        file_path = os.path.join("wwwroot", path[1:])
        
#################################################################

        #memeriksa apakah file ada dalam sistem
        if os.path.exists(file_path) and os.path.isfile(file_path):

            #menerima ukuran dari file yang diminta
            file_size = os.path.getsize(file_path)

            #untuk menerima MIME yang diminta dari file extension
            mime_type, _ = mimetypes.guess_type(file_path)

            #line ini membuat respons dari header yang akan dikirim ke client dengan status OK
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: " + mime_type + "\r\n"
            response += "Content-Length: " + str(file_size) + "\r\n"
            response += "\r\n"
             #mengirim HTTP respons ke client berbentuk bytes menggunakan metode 'client_socket.send()'
            client_socket.send(response.encode())

            #meminta file dengan ukuran 1024 bytes dan mengirimnya menggunakan metode 'client_socket.send()'
            with open(file_path, 'rb') as f:
                while True:
                    file_data = f.read(1024)
                    if not file_data:
                        break
                    client_socket.send(file_data)

        #memanggil link html ketika file html tidak ditemukan
        else:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type: text/html\r\n"
            response += "\r\n"
            response += "<html><body><h1>404 Not Found</h1></body></html>"
            client_socket.send(response.encode())
            
    #menutup socket
    client_socket.close()
