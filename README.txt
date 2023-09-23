RUBRIC

1. The server successfully accepts multiple client connections simultaneously.

    This condition is met. Whatever the user chooses for number of max clients, 
    those many clients are accepted and served concurrently by the server. 
    If the user tries to enter too many clients at once, a message is displayed:
    "Max clients reached. Waiting for a client to disconnect."
    The program then waits until one or more clients have disconnected before accepting new ones.
    If the server is closed while it is running using a keyboard interrupt, a message
    is displayed: "Server shut down."

2. The server successfully receives HTTP GET requests, parses, and handles them correctly.

    This condition is met. Whenever the client command is executed, the exact file
    (assuming it exists) is saved onto the working directory with all its contents.

3. The server sends the appropriate HTTP response.

    This condition is met. If the client command runs and the file exists, the response:
    "HTTP/1.1 200 OK" is displayed. In the next line, a message is displayed:
    "saved filename: existingfilename"
    Once again, in the next line, a message is displayed:
    "Response saved as: existingfilename"
    where "existingfilename" represents whatever name was given in the request header

    If file doesn't exist, the message: "HTTP/1.1 404 NOT FOUND" is displayed.
    In the next line, the messsage "File not found." is displayed.
    Client doesn't end up connecting to the server in this case.

4. The server handles client disconnections.

    This condition is met. If a client disconnects, even if the user tries to 
    connect too many clients at the same time and the 
    "Max clients reached. Waiting for a client to disconnect." 
    message is displayed, the second one or more users disconnect, the server
    starts to accept new connections again.
    If the client connection is interrupted using a keyboard interrupt while
    trying to connect to the server, a message is displayed:
    "Client has interrupted the connection."

5. The client can connect to the server.

    This condition is met. The second a client connects, 
    a message is displayed on the server side: "Accepted connection from: IP_ADDRESS"

6. The client can send HTTP GET requests to the server.

    This condition is met. The client gets and saves the requested file once the GET request is sent
    (assuming it exists)

7. The client receives the HTTP response from the server and parses it correctly to save the received
   file.

    This condition is met.
    Once the HTTP response is received, the requested file is saved onto the client side.
    Since each client is unique, the file they request will each have a unique timestamp,
    so the user knows each file is being requested from a different client.
