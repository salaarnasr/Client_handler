import socket
import sys
import time


def main():
    try:  # Try block to catch KeyboardInterrupt
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

        status_line, body = response.split("\r\n", 1)
        print(status_line)  # Print the status line immediately

        if "503 Service Unavailable" in response:
            print("Server busy: Max clients reached.")
        elif "404 NOT FOUND" in response:
            print("File not found.")
        else:
            # Save the response with a unique filename using a timestamp
            timestamp = str(int(time.time()))
            save_filename = f"{timestamp}_{filename}"
            print("Saved filename:", save_filename)
            with open(save_filename, "w") as file:
                file.write(body)
            print(f"Response saved as: {save_filename}")
            print("Client successfully disconnected")

        client_socket.close()

    except KeyboardInterrupt:  # Catch KeyboardInterrupt here
        print("\nClient has interrupted the connection.")


if __name__ == "__main__":
    main()
