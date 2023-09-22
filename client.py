import socket
import sys
import time


def main():
    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <PORT> <FILENAME>")
        sys.exit(1)

    # Retrieve command line arguments
    port = int(sys.argv[1])
    filename = sys.argv[2]

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server on localhost and the given port
    client_socket.connect(("127.0.0.1", port))

    # Construct and send the HTTP GET request
    request = f"GET /{filename} HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\n\r\n"
    client_socket.send(request.encode())

    # Receive the response from the server
    response = client_socket.recv(4096).decode()

    if "503 Service Unavailable" in response:
        print("Server busy: Max clients reached.")
    else:
        # Save the response with a unique filename using a timestamp
        timestamp = str(int(time.time()))
        save_filename = f"received_{timestamp}_{filename}"
        with open(save_filename, "w") as file:
            file.write(response)
        print(f"Response saved as {save_filename}")

    print("disconnected")
    client_socket.close()


if __name__ == "__main__":
    main()
