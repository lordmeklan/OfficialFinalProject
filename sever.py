import sqlite3
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

DATABASE = 'userdatabase.db'  # Define the database file

def init_db():
    """ Initialize the database and create the userdata table if it doesn't exist """
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS userdata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='text/plain'):
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        if self.path == '/login':
            self.handle_login()
        elif self.path == '/register':
            self.handle_register()
        else:
            self._set_headers(404)
            self.wfile.write(b'Not Found')

    def handle_login(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        username = data['username']
        password = hashlib.sha256(data['password'].encode()).hexdigest()

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

        if cur.fetchone():
            self._set_headers(200, 'application/json')
            self.wfile.write(json.dumps({'message': 'Login Successful'}).encode())
        else:
            self._set_headers(401, 'application/json')
            self.wfile.write(json.dumps({'message': 'Login Failed'}).encode())
        conn.close()

    def handle_register(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        username = data['username']
        password = hashlib.sha256(data['password'].encode()).hexdigest()

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM userdata WHERE username = ?", (username,))

        if cur.fetchone():
            self._set_headers(409, 'application/json')
            self.wfile.write(json.dumps({'message': 'Username already exists.'}).encode())
        else:
            cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            self._set_headers(201, 'application/json')
            self.wfile.write(json.dumps({'message': 'Registration Successful'}).encode())
        conn.close()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=9999):
    init_db()  # Initialize the database when the server starts
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
