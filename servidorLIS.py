import socket
import os
class ServidorLIS:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = None

    def iniciar_servidor(self):
        # Crear el socket del servidor
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        carpeta = "C:\\interfaz_netlabsx"
        archivo = "C:\\interfaz_netlabsx\\listener.txt"
        with open(archivo, "w") as file:
            file.write("------------------ INICIO DE LA INTERFAZ ------------------\n")
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        with open(archivo, "a") as file:
            file.write("Nuevo contenido del archivo\n")
            file.write("Más texto agregado\n")

        try:
            # Vincular el socket a la dirección IP y puerto
            self.server_socket.bind((self.ip, self.port))

            # Escuchar conexiones entrantes
            self.server_socket.listen(1)
            print("Servidor LIS en ejecución. Esperando conexiones...")

            while True:
                # Aceptar la conexión entrante
                client_socket, client_address = self.server_socket.accept()
                print(f"Conexión establecida con {client_address}")

                # Recibir datos del cliente
                data = client_socket.recv(2048)
                file.write("---------------------------------\n")
                file.write(data)
                file.write("FIN---------------------------------\n")
                received_data = data.decode()
                #print(f"Datos recibidos del cliente: {received_data}")

                # Realizar el procesamiento necesario con los datos recibidos

                # Enviar respuesta al cliente (opcional)
                response = "Datos recibidos correctamente"
                client_socket.sendall(response.encode())

                # Cerrar la conexión con el cliente
                client_socket.close()

        except KeyboardInterrupt:
            print("Interrupción del usuario. Cerrando el servidor LIS.")

        finally:
            # Cerrar el socket del servidor
            self.server_socket.close()

# Uso de la clase ServidorLIS
if __name__ == '__main__':
    server_ip = '192.168.1.97'  # Dirección IP del servidor
    server_port = 7118  # Puerto del servidor

    servidor = ServidorLIS(server_ip, server_port)
    servidor.iniciar_servidor()