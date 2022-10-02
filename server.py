# server.py

#import unicorn_tools as uni
import socket
import _thread
import threading
from queue import Queue

HOST = "0.0.0.0"  # force ipv4
PORT = 25565

print_lock = threading.Lock()
uni_lock = threading.Lock()

q = Queue()

def unicorn_thread():
    while True:
        msg = q.get()
        uni_lock.acquire()
        print(msg)
        uni_lock.release()

def client_thread(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
        except:
            t_print(f"{str(addr)} connection lost.")
            break
        else:
            if not data:
                t_print(f"{str(addr)} connection closed.")
                break
            t_print(f"Received: {str(decode(data))} from {str(addr)}")
            q.put(decode(data))
            
            conn.send(encode(f"Message {decode(data)} placed in queue"))
        
    conn.close()

def t_print(msg):
    print_lock.acquire()
    print(msg)
    print_lock.release()

def encode(msg):
    return msg.encode("ascii")

def decode(msg):
    return msg.decode("ascii")

def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    _thread.start_new_thread(unicorn_thread, ())
    conn_list = list()
    print("Server started on port", PORT)

    while True:
        try:
            conn, addr = s.accept()
            _thread.start_new_thread(client_thread, (conn, addr))
            conn_list.append(conn)
            t_print(f"Connected to {str(addr)}")
        except KeyboardInterrupt:
            print("Server shutting down")
            break

    (c.close() for c in conn_list)
    s.close()

if __name__ == "__main__":
    run()
