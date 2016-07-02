import socket

HOST = "localhost"
PORT = 8001

def main():
    # IPv4(AF_INET)でTCP(SOCK_STREAM)を使ったソケットをつくる
    # http://blog.livedoor.jp/shf0811/archives/6841382.html
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))
    server.listen(1)

    print("クライアントからの接続を待ちます。")
    client_socket, client_address = server.accept()
    print("クライアント接続。")

    # バッファサイズ1024で、clientと接続しているソケットを使ってデータを受信
    # なお、書籍では"0"を終了マークとしているが、ここでは実装しない
    byte_msg = client_socket.recv(1024)

    # クライアントから受け取った内容をserver_recv.txtに出力
    # バイト列で受信しているので、ファイルに保存できるよう文字列へデコード
    # http://python.civic-apps.com/python3-bytes-str-convert/
    str_msg = byte_msg.decode("utf-8")
    # 念のため、コマンドプロンプト上にも表示
    print(str_msg)
    with open("./file/server_recv.txt", mode="w", encoding="utf-8") as f:
        f.write(str_msg)

    # server_send.txtの内容をクライアントに送付
    with open("./file/server_send.txt", encoding="utf-8") as f:
        data = f.read()
        # Pythonでsocketを使ってデータ送信する場合、バイト列にする必要があるため、
        # utf-8などでエンコードしておく
        client_socket.send(data.encode("utf-8"))

    client_socket.close()
    print("通信を終了しました。")
    server.close()


if __name__ == "__main__":
    main()