import socket

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('raspberry_pi_ip_address', 5555)) #replace 'raspberry_pi_ip_address with rasppi address

try:
    while True:
        # You can implement remote control logic here
        pass

except KeyboardInterrupt:
    client_socket.close()
