import socket
import threading
import sys
import time

# Initializing global variables to keep track of client count and limit.
active_clients = 0
max_clients = 0
client_lock = threading.Lock()  # A lock to handle concurrent updates to active_clients.


# Function to handle individual client connections.
def handle_client(client_socket):
    global active_clients  # Declare active_clients as global as we are modifying it inside this function.

    # Receiving and decoding the client request.
    request = client_socket.recv(1024).decode()

    # Extracting headers and filename from the client request.
    headers = request.split("\n")
    filename = headers[0].split()[1]
    filename = filename[1:]  # Removing the leading slash

    time.sleep(5)  # Delay to simulate processing time.

    try:
        # Trying to open and read the requested file.
        with open(filename, "rb") as f:
            content = f.read()

        # Preparing and sending a positive HTTP response.
        response = "HTTP/1.1 200 OK\r\n\r\n".encode()
        client_socket.send(response + content)
    except FileNotFoundError:
        # Handling the case when the requested file is not found.
        response = "HTTP/1.1 404 NOT FOUND\r\n\r\nFile Not Found".encode()
        client_socket.send(response)

    # Reducing the count of active clients as the request is processed.
    active_clients -= 1
    client_socket.close()  # Closing the client socket.


def main():
    try:
        global active_clients, max_clients  # Declare as global since we're modifying them.

        # Validating the command-line arguments.
        if len(sys.argv) != 3:
            print("Usage: server.py SERVER_PORT MAX_CLIENTS")
            exit(1)

        # Setting up the maximum allowed clients.
        max_clients = int(sys.argv[2])

        # Creating and binding the server socket.
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", int(sys.argv[1])))
        server.listen(max_clients)

        # Displaying server information.
        print(f"[*] Listening on 127.0.0.1:{sys.argv[1]}")
        print(f"[*] Max clients: {max_clients}")

        while True:
            # Accepting a new client connection.
            client, addr = server.accept()

            if active_clients < max_clients:
                # If the limit is not reached, spawn a new thread to handle the client.
                print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
                active_clients += 1
                client_handler = threading.Thread(target=handle_client, args=(client,))
                client_handler.start()
            else:
                # If the maximum client limit is reached, send an error response.
                print("Max clients reached. Waiting for a client to disconnect.")
                response = "HTTP/1.1 503 Service Unavailable\r\n\r\nMax clients reached.".encode()
                client.send(response)
                client.close()
    except KeyboardInterrupt:
        # Handling the case when the server is interrupted by keyboard input.
        print("\nServer shut down.")


if __name__ == "__main__":
    main()  # Invoking the main function to run the server.
