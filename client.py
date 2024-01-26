# Import necessary libraries
import socket
import json


def send_message(message, server_address=('localhost', 1234)):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message_data = json.dumps(message).encode('utf-8')
    client_socket.sendto(message_data, server_address)

    data, server_address = client_socket.recvfrom(4096)
    response = json.loads(data.decode('utf-8'))
    client_socket.close()

    return response


def register_user(name, surname, email, phone):
    message = {
        "type": "register_user",
        "user_info": {"name": name, "surname": surname, "email": email, "phone": phone}
    }
    return send_message(message)


def delete_user(email, phone):
    message = {
        "type": "delete_user",
        "email": email,
        "phone": phone
    }
    return send_message(message)


def get_users():
    message = {"type": "get_users"}
    return send_message(message)


# Example usage
register_user("Raw", "Arnaud", "raw.arnaud@email.com", "123456987")
register_user("Richard", "Petion", "richard.petion@email.com", "123450976")
get_users_response = get_users()
print("Registered Users:", get_users_response["users"])

delete_user_response = delete_user("raw.arnaud@email.com", "123456987")
print(delete_user_response)

get_users_response = get_users()
print("Registered Users After First Deletion:", get_users_response["users"])
delete_user_response = delete_user("richard.petion@email.com", "123450976")
print(delete_user_response)

get_users_response = get_users()
print("Registered Users After Second Deletion", get_users_response["users"])
