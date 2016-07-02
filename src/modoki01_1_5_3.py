import socket
from email.utils import formatdate

HOST = "localhost"
PORT = 8001
DOCUMENT_ROOT = "D:/Sandbox/syakyo_create_web_server/src/static"

def write_line(sock, str_data):
    data = str_data + "\r\n"
    byte_data = data.encode("utf-8")
    sock.send(byte_data)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print("クライアントからの接続を待ちます")
    client_socket, client_address = server.accept()

    byte_msg = client_socket.recv(1024)
    str_msg = byte_msg.decode("utf-8")
    # 念のため、コマンドプロンプト上にも表示
    print(str_msg)

    # HTTPリクエストヘッダはCRLFで改行されるため、それを目印に行ごとに分ける
    lines = str_msg.split("\r\n")
    for line in lines:
        if line.startswith("GET"): #=> GET /index.html HTTP/1.1
            path = line.split(" ")[1] # => /index.html

    
    # レスポンスヘッダを返す
    write_line(client_socket, "HTTP/1.1 200 OK")
    # http://stackoverflow.com/questions/225086/rfc-1123-date-representation-in-python
    write_line(client_socket, formatdate(usegmt=True))
    write_line(client_socket, "Server: Modoki/0.1")
    write_line(client_socket, "Connection: close")
    write_line(client_socket, "Content-Type: text/html")
    write_line(client_socket, "")

    # レスポンスボディを返す
    with open(DOCUMENT_ROOT + path, encoding="utf-8") as f: 
        r = f.read()
        write_line(client_socket, r)
        
    client_socket.close()
    server.close()


if __name__ == "__main__":
    main()