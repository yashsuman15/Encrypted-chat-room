import socket
import threading

PORT = 8000
HOST = socket.gethostbyname(socket.gethostname())

choice = input('Do you want to HOST :->> PRESS (1) \nDo you want to CONNECT :->> PRESS (2) \n-->')
nickname = input("Enter your nickname: ")

if choice == "1":
    # Server Code
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    clients = []
    nicknames = []

    def broadcast(message):
        for client in clients:
            client.send(message)

    def handle(client):
        while True:
            try:
                message = client.recv(1024)
                broadcast(message)
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat!'.encode('ascii'))
                nicknames.remove(nickname)
                break

    def receive():
        while True:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            print(f"Nickname of the client is {nickname}!")
            broadcast(f"{nickname} joined the chat!".encode('ascii'))
            client.send('Connected to the server!'.encode('ascii'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

    print("Server is listening...")
    receive()

elif choice == "2":
    # Client Code
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    ###############################
    # HOST = input("enter ip address")
    ###############################
    client.connect((HOST, PORT))

    def receive():
        while True:
            try:
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(nickname.encode('ascii'))
                else:
                    print(message)
            except:
                print("An error occurred!")
                client.close()
                break

    def write():
        while True:
            message = f'{nickname}: {input("")}'
            client.send(message.encode('ascii'))

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

else:
    print("Invalid choice. Exiting.")
    exit()