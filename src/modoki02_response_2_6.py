
import os
import email.utils
import modoki02_util_2_6

def send_ok_response(sock, full_path, ext):
    # htmlが文字化けしたので、charsetを追加した
    modoki02_util_2_6.write_line(sock, "HTTP/1.1 200 OK")
    modoki02_util_2_6.write_line(sock, email.utils.formatdate(usegmt=True))
    modoki02_util_2_6.write_line(sock, "Server: Modoki/0.2")
    modoki02_util_2_6.write_line(sock, "Connection: close")

    content_type = "Content-Type: {}".format(modoki02_util_2_6.get_content_type(ext))
    modoki02_util_2_6.write_line(sock, content_type)
    modoki02_util_2_6.write_line(sock, "")

    if "text" in content_type:
        with open(full_path, encoding="utf-8") as f:
            r = f.read()
            modoki02_util_2_6.write_line(sock, r)
    
    elif "image" in content_type:
        with open(full_path, mode="rb") as f:
            r = f.read()
            sock.send(r)


def send_move_permanently_response(sock, location):
    # Chromeの場合、301ではキャッシュすることもあるので注意
    # http://d.hatena.ne.jp/too_young/20110303/1299149420
    modoki02_util_2_6.write_line(sock, "HTTP/1.1 301 Moved Permanently")
    modoki02_util_2_6.write_line(sock, "Date: {}".format(email.utils.formatdate(usegmt=True)))
    modoki02_util_2_6.write_line(sock, "Server: Modoki/0.2")
    modoki02_util_2_6.write_line(sock, "Location: {}".format(location))
    modoki02_util_2_6.write_line(sock, "Connection: close")
    modoki02_util_2_6.write_line(sock, "")


def send_not_found_response(sock, error_document_root):
    modoki02_util_2_6.write_line(sock, "HTTP/1.1 404 Not Found")
    modoki02_util_2_6.write_line(sock, "Date: {}".format(email.utils.formatdate(usegmt=True)))
    modoki02_util_2_6.write_line(sock, "Server: Modoki/0.2")
    modoki02_util_2_6.write_line(sock, "Connection: close")
    modoki02_util_2_6.write_line(sock, "Content-type: text/html")
    modoki02_util_2_6.write_line(sock, "")

    error_full_path = os.path.join(error_document_root, "404.html")
    with open(error_full_path, encoding="utf-8") as f:
        r = f.read()
        modoki02_util_2_6.write_line(sock, r)


def send_directory_traversal_response(sock, error_document_root):
    modoki02_util_2_6.write_line(sock, "HTTP/1.1 404 Not Found")
    modoki02_util_2_6.write_line(sock, "Date: {}".format(email.utils.formatdate(usegmt=True)))
    modoki02_util_2_6.write_line(sock, "Server: Modoki/0.2")
    modoki02_util_2_6.write_line(sock, "Connection: close")
    modoki02_util_2_6.write_line(sock, "Content-type: text/html")
    modoki02_util_2_6.write_line(sock, "")

    error_full_path = os.path.join(error_document_root, "404_dir_traversal.html")
    with open(error_full_path, encoding="utf-8") as f:
        r = f.read()
        modoki02_util_2_6.write_line(sock, r)
