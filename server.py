import socket
import threading
import sys
import time

active_clients = 0
max_clients = 0
client_lock = threading.Lock()


def handle_client(client_socket):
    global active_clients
    request = client_socket.recv(1024).decode()

    headers = request.split("\n")
    filename = headers[0].split()[1]
    filename = filename[1:]
    time.sleep(5)

    try:
        with open(filename, "rb") as f:
            content = f.read()
        response = "HTTP/1.1 200 OK\r\n\r\n".encode()
        client_socket.send(response + content)
    except FileNotFoundError:
        response = "HTTP/1.1 404 NOT FOUND\r\n\r\nFile Not Found".encode()
        client_socket.send(response)

    active_clients -= 1
    client_socket.close()


def main():
    try:
        global active_clients, max_clients

        if len(sys.argv) != 3:
            print("Usage: server.py SERVER_PORT MAX_CLIENTS")
            exit(1)

        max_clients = int(sys.argv[2])

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", int(sys.argv[1])))
        server.listen(max_clients)

        print(f"[*] Listening on 127.0.0.1:{sys.argv[1]}")
        print(f"[*] Max clients: {max_clients}")

        while True:
            client, addr = server.accept()

            if active_clients < max_clients:
                print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
                active_clients += 1
                client_handler = threading.Thread(target=handle_client, args=(client,))
                client_handler.start()
            else:
                pass
                print("Max clients reached. Waiting for a client to disconnect.")
                response = "HTTP/1.1 503 Service Unavailable\r\n\r\nMax clients reached.".encode()
                client.send(response)
                client.close()
    except KeyboardInterrupt:
        print("\nServer shut down.")


if __name__ == "__main__":
    main()
