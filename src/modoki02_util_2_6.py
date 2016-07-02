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