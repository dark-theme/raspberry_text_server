# client.py

import socket
import _thread

HOST = "xxx.xx.xxx.xxx"
PORT = 25571

FG = "(255, 255, 255)"
BG = "(0, 0, 0)"

# FG;BG;MSG

def client(s: socket):
    while True:
        try:
            data = s.recv(1024)
        except:
            print("Server closed")
            break
        else:
            if not data:
                print("Server closed")
                break
            print(f"\nServer: {decode(data)}")
        
    s.close()
    exit()

def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    t = _thread.start_new_thread(client, (s,))

    while True:
        try:
            msg = input("Send: ")
            s.send(encode(f"{FG};{BG};{msg}"))
            
        except KeyboardInterrupt:
            print("Shutting down")
            break
        
    s.close()

def encode(msg: str) -> bytes:
    return msg.encode("ascii")

def decode(msg: bytes) -> str:
    return msg.decode("ascii")

if __name__ == "__main__":
    run()
