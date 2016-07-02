import socket
import threading
import os
import urllib.parse
import modoki02_response_2_6

HOST = "localhost"
PORT = 8001
DOCUMENT_ROOT = "D:/Sandbox/syakyo_create_web_server/src/static"
SERVER_NAME = "{host}:{port}".format(host=HOST, port=PORT)


def server_thread(sock):
    try:
        byte_msg = sock.recv(1024)
        str_msg = byte_msg.decode("utf-8")
        if not str_msg:
            return
        # 念のため、コマンドプロンプト上にも表示
        print(str_msg)

        lines = str_msg.split("\r\n")
        for line in lines:
            if line.startswith("GET"):
                # Python3の場合、標準ライブラリでデコードできる
                # http://docs.python.jp/3/library/urllib.parse.html#urllib.parse.unquote
                # http://stackoverflow.com/questions/16566069/url-decode-utf-8-in-python
                path = urllib.parse.unquote(line.split(" ")[1]) #=> /index.html
                root, ext = os.path.splitext(path) 
                ext = ext.lstrip(".")
            elif line.startswith("Host:"):
                # リダイレクトするときに使うため、ホスト名を取得しておく
                # "Host: host_name" => " host_name" => "host_name"  
                host = line.lstrip("Host:").strip()

        if not path:
            return

        # ディレクトリ指定時にindex.htmlを返すようにする
        if path.endswith("/"):
            path += "index.html"
            ext = "html"

        # ディレクトリトラバーサル対策
        if not os.path.abspath(path):
            print("指定された {} はディレクトリトラバーサルです".format(path))
            modoki02_response_2_6.send_directory_traversal_response(sock, DOCUMENT_ROOT)
            return

        # 指定されたファイルのフルパスを取得
        # http://stackoverflow.com/questions/1854/python-what-os-am-i-running-on
        if os.name == "nt":
            # Windowsの場合、ファイルの絶対パスは単純なos.path.join()では取得できない
            # http://stackoverflow.com/questions/2422798/python-os-path-join-on-windows
            print("normal join: {}".format(os.path.join(DOCUMENT_ROOT, path)))
            #=> D:/index.html
            docroot_drive = DOCUMENT_ROOT[0:2]
            docroot_path = DOCUMENT_ROOT[2:]
            full_path = os.path.join(docroot_drive, os.sep, docroot_path + path)
            print("fullpath: {}".format(full_path))
            #=> D:/Sandbox/syakyo_create_web_server/src/static/index.html
        else:
            # テストしてない...
            full_path = os.path.join(DOCUMENT_ROOT, path)

        # 存在しないファイルが指定された場合、404を表示
        if not os.path.exists(full_path):
            print("ファイル {} は存在しません".format(full_path))
            modoki02_response_2_6.send_not_found_response(sock, DOCUMENT_ROOT)
            return

        # ディレクトリが指定された場合、末尾に"/"を付けて301リダイレクト
        if os.path.isdir(full_path):
            host_name = host if host else SERVER_NAME
            location = "http://{host}{path}/".format(
                host=host_name,
                path=path
            )
            print("次のlocationにリダイレクトします => {}".format(location))
            modoki02_response_2_6.send_move_permanently_response(sock, location)
            return

        modoki02_response_2_6.send_ok_response(sock, full_path, ext)

    finally:
        sock.close()
        print("-" * 10)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print("クライアントからの接続を待ちます")
    # KeyboardInterruptせず、Breakキーで代用
    # http://stackoverflow.com/questions/15189888/python-socket-accept-in-the-main-thread-prevents-quitting
    try:
        while True:
            client_socket, client_address = server.accept()
            thread = threading.Thread(
                target=server_thread,
                # client_addressは使わないので、渡さない
                # また、argsは引数一つであってもタプルで指定しないとエラーになる
                args=((client_socket, )))
            thread.start()

    finally:
        server.close()


if __name__ == "__main__":
    main()