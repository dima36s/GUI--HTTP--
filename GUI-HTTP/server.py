import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Создание базы данных
conn = sqlite3.connect('mydb.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS records
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, address TEXT)''')
conn.commit()
conn.close()


# Обработчик HTTP-запросов на сервере
class ServerHandler(BaseHTTPRequestHandler):
    def _send_response(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(message).encode())

    def do_GET(self):
        if self.path == '/get_records':
            conn = sqlite3.connect('mydb.db')
            c = conn.cursor()
            c.execute("SELECT * FROM records")
            records = c.fetchall()
            conn.close()
            records_json = []
            for record in records:
                record_dict = {
                    'id': record[0],
                    'name': record[1],
                    'age': record[2],
                    'address': record[3]
                }
                records_json.append(record_dict)
            self._send_response(records_json)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Error 404: Not Found')

    def do_POST(self):
        if self.path == '/add_record':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            record = json.loads(post_data)
            conn = sqlite3.connect('mydb.db')
            c = conn.cursor()
            c.execute("INSERT INTO records (name, age, address) VALUES (?, ?, ?)",
                      (record['name'], record['age'], record['address']))
            conn.commit()
            conn.close()
            self._send_response({'message': 'Record added successfully'})
        elif self.path == '/delete_record':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            record_id = json.loads(post_data)['id']
            conn = sqlite3.connect('mydb.db')
            c = conn.cursor()
            c.execute("DELETE FROM records WHERE id=?", (record_id,))
            conn.commit()
            conn.close()
            self._send_response({'message': 'Record deleted successfully'})
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Error 404: Not Found')


# Запуск сервера
def run():
    PORT = 8000
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, ServerHandler)
    print(f'Starting server on port {PORT}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
