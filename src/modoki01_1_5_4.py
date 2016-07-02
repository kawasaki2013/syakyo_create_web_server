import socket
from email.utils import formatdate
import os
import threading

HOST = "localhost"
PORT = 8001
DOCUMENT_ROOT = "D:/Sandbox/syakyo_create_web_server/src/static"

# 拡張子とContent-Typeの対応表
CONTENT_TYPE_MAP = {
    "html": "text/html",
    "htm": "text/html",
    "txt": "text/plain",
    "css": "text/css",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
}

def get_content_type(ext):
    '''拡張子を受け取り、Content-Typeを返す'''
    if ext in CONTENT_TYPE_MAP:
        return CONTENT_TYPE_MAP[ext]
    elif ext.lower() in CONTENT_TYPE_MAP:
        return CONTENT_TYPE_MAP[ext.lower()]
    else:
        return "application/octet-stream"


def write_line(sock, str_data):
    data = str_data + "\r\n"
    byte_data = data.encode("utf-8")
    sock.send(byte_data)


def server_thread(sock, address):
    try:
        byte_msg = sock.recv(1024)
        str_msg = byte_msg.decode("utf-8")
        # 念のため、コマンドプロンプト上にも表示
        print(str_msg)

        lines = str_msg.split("\r\n")
        for line in lines:
            if line.startswith("GET"): #=> GET /index.html HTTP/1.1
                path = line.split(" ")[1] # => /index.html
                root, ext = os.path.splitext(path) # => (ext) .html
                ext = ext.lstrip(".") # => html

        
        # レスポンスヘッダを返す
        write_line(sock, "HTTP/1.1 200 OK")
        write_line(sock, formatdate(usegmt=True))
        write_line(sock, "Server: Modoki/0.1")
        write_line(sock, "Connection: close")
        content_type = get_content_type(ext)
        write_line(sock, "Content-Type: {}".format(content_type))
        write_line(sock, "")

        # レスポンスボディを返す
        # Java版とは異なり、textとimageは同じようには扱えないため、分けて処理する
        if "text" in content_type:
            with open(DOCUMENT_ROOT + path, encoding="utf-8") as f:
                r = f.read()
                write_line(sock, r)
        elif "image" in content_type:
            with open(DOCUMENT_ROOT + path, mode="rb") as f: 
                r = f.read()
                # 画像の場合、読み込んだバイナリに改行コードを加えてはいけないので、そのまま送る
                sock.send(r)
    
    finally:
        sock.close()



def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print("クライアントからの接続を待ちます")

    try:
        while True:
            # accept()中にCtrl+Cを押しても受け付けないため、
            # Breakキーで強制的に停止させる
            client_socket, client_address = server.accept()

            thread = threading.Thread(
                target=server_thread,
                args=(client_socket, client_address))
            thread.start()
    finally:
        server.close()


if __name__ == "__main__":
    main()