import socket

def dhcp_server():
	server_ip = '127.0.0.1' # It must be your IP address ==> '192.168.1.100'
	server_port = 7000
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
		server_socket.bind((server_ip, server_port))
		print(f"DHCP server listening on {server_ip}: {server_port}")
		while True:
			data, client_address = server_socket.recvfrom(1024)
			print(f"Recceived request from {client_address}: {data.decode()}")
			response = "Assigned IP: 192.168.1.101"
			server_socket.sendto(response.encode(), client_address)

if __name__ == "__main__":
	dhcp_server()
			