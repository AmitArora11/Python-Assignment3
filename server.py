# Import necessary libraries
import socket
import json


# Function to create user
def handle_register_user(data, users):
    user_info = data["user_info"]
    user_key = f"{user_info['email']}_{user_info['phone']}"
    if user_key in users:
        users[user_key].update(user_info)
    else:
        users[user_key] = user_info
    return {"status": "success"}


# Function to delete user
def handle_delete_user(data, users):
    user_key = f"{data['email']}_{data['phone']}"
    if user_key in users:
        del users[user_key]
        return {"status": "success"}
    else:
        return {"status": "user not found"}


# Function to get list of user
def handle_get_users(users):
    return {"users": list(users.values())}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 1234)
    server_socket.bind(server_address)

    users = {}

    while True:
        data, client_address = server_socket.recvfrom(4096)
        decoded_data = json.loads(data.decode('utf-8'))

        if decoded_data["type"] == "register_user":
            response = handle_register_user(decoded_data, users)
        elif decoded_data["type"] == "delete_user":
            response = handle_delete_user(decoded_data, users)
        elif decoded_data["type"] == "get_users":
            response = handle_get_users(users)
        else:
            response = {"status": "unknown request"}

        response_data = json.dumps(response).encode('utf-8')
        server_socket.sendto(response_data, client_address)


server()
