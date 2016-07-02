import socket

HOST = "localhost"
PORT = 8001

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # client_send.txtの内容をサーバに送信
    # "0"の送信は実装しない
    # http://diveintopython3-ja.rdy.jp/files.html
    with open("./file/client_send.txt", encoding="utf-8") as f: 
        data = f.read()
        client.send(data.encode("utf-8"))

    # サーバからの返信をclient_recv.txtに出力
    byte_msg = client.recv(4096)
    str_msg = byte_msg.decode("utf-8")
    # 念のため、コマンドプロンプト上にも表示
    print(str_msg)
    with open("./file/client_recv.txt", mode="w", encoding="utf-8") as f:
        f.write(str_msg)


if __name__ == "__main__":
    main()