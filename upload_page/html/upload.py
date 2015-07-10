from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import time
import os


class MyServer(BaseHTTPRequestHandler):

    def _get_mime(self, path):
        if os.path.splitext(path)[1] == '.css':
            return "text/css"
        elif os.path.splitext(path)[1] == '.ico':
            return "image/x-icon"
        elif os.path.splitext(path)[1] == '.html':
            return "text/html"
        return ""

    def _get_abs_filepath(self, path):
        file_path = os.path.basename(path)
        if file_path == "":
            file_path = "index.html"
        return file_path

    def _handle_body(self, line):
        f = open("2.jpg", mode="ab")
        f.write(line)
        f.close()

    def _handle_a_line(self, line):
        boundary = str.encode(self._boundary)
        if line.find(boundary) != -1:
            if self._status_boundary == "OUT":
                self._status_boundary = "IN"
            elif self._status_boundary == "IN":
                self._status_boundary = "OUT"
                self._status_content = "HEAD"
            return

        if line == b"\r\n":
            if self._status_content == "HEAD":
                self._status_content = "BODY"
            elif self._status_content == "BODY":
                self._status_content = "HEAD"
            return

        if self._status_boundary == "OUT":
            return

        if self._status_content == "HEAD":
            [k, v] = line.split(b": ")
        elif self._status_content == "BODY":
            self._handle_body(line)

    def do_GET(self):
        file_path = self._get_abs_filepath(self.path)
        f = open(file_path, "rb", buffering=0)

        self.send_response(200)
        self.send_header("Content-type", self._get_mime(self.path))
        self.end_headers()
        self.wfile.write(f.readall())

    def do_POST(self):
        content_length = int(self.headers.get_all('Content-Length')[0])
        content_type = self.headers.get_all('Content-Type')[0]
        self._boundary = content_type.split('boundary=', maxsplit=1)[1]
        self.buf = b''
        self._status_boundary = "OUT"  # OUT, IN
        self._status_content = "HEAD"  # HEAD, BODY

        new_line = ''
        buf = ''

        while content_length > 0:
            want_byte = 4096
            if content_length > want_byte:
                buf = self.rfile.read(want_byte)
            else:
                buf = self.rfile.read(content_length)
            content_length -= want_byte
            self.buf = self.buf + buf

            while True:
                line_end = self.buf.find(b'\r\n')
                if line_end == -1:
                    break
                else:
                    self._handle_a_line(self.buf[:line_end + 2])
                    self.buf = self.buf[line_end + 2:]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


class ForkingHTTPServer(socketserver.ForkingMixIn, HTTPServer):

    def finish_request(self, request, client_address):
        HTTPServer.finish_request(self, request, client_address)

if __name__ == "__main__":
    try:
        s = ForkingHTTPServer(("0.0.0.0", 80), MyServer)
        s.serve_forever()
    except KeyboardInterrupt:
        s.socket.close()