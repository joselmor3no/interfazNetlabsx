import os
import time
import sched
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk, scrolledtext
from threading import Thread

from hilos import *
from ftplib import FTP



class GraficosNet(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x650')
        self.resizable(0, 0)
        self.title('Interfaz de Química Sanguinea | NetLabsx')
        self.iconbitmap('C:/interfaz_netlabsx/iconoPrincipal.ico')
        self.entrada = None
        self.entrada_texto = tk.StringVar()
        self.barra_progreso = None
        self.caja_texto = None
        self.label_archivoc = tk.Label()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self._creacion_componentes()  # Llamar a _creacion_componentes antes de insertar texto
        self.archivoTexto = "C:\\interfaz_netlabsx\\listener.txt"
        self.scheduler_thread = None


    def upload_file(self):
        # Configurar la conexión FTP
        hostname = "ftp.netlabsx.com"
        username = "ftp_victoria_lab@netlabsx.com"
        password = "***"
        remote_filename = "sucursal139qui.txt"
        local_file_path = "C:\\interfaz_netlabsx\\sucursal139qui.txt"

        try:
            # Obtener el tamaño total del archivo
            total_size = os.path.getsize(local_file_path)

            # Crear una instancia del objeto FTP
            ftp = FTP()

            # Conectarse al servidor FTP
            ftp.connect(hostname)
            ftp.login(username, password)

            # Abrir el archivo local en modo de lectura binaria
            with open(local_file_path, "rb") as file:
                # Subir el archivo al servidor FTP
                ftp.storbinary(f"STOR {remote_filename}", file,
                               callback=self.upload_callback(total_size))

            # Cerrar la conexión FTP
            ftp.quit()

            time.sleep(1)
            self.barra_progreso['value'] = 0
            fecha_hora_actual = self.obtener_fecha_hora_actual()
            self.label_archivoc.config(text=fecha_hora_actual)
            self.update_idletasks()
            print(
                f"El archivo '{local_file_path}' se ha subido correctamente a '{hostname}/{remote_filename}'. {fecha_hora_actual}")
        except Exception as e:
            print(f"No se pudo subir el archivo: {str(e)}")

    def obtener_fecha_hora_actual(self):
        from datetime import datetime
        fecha_hora = datetime.now()
        return str(f'Fecha de utima subida: {fecha_hora}')

    def upload_callback(self, total_size):
        def callback(chunk):
            self.barra_progreso['value'] += len(chunk)
            self.update_idletasks()

        return callback

    def schedule_upload(self):
        while True:
            self.upload_file()
            # Esperar 5 minutos antes de la próxima ejecución
            time.sleep(300)

    def _conectar_servidor(self):

        servidor_thread = ServidorLISThread()
        servidor_thread.start()

        file_watcher_thread = FileWatcherThread()
        file_watcher_thread.start()

        self.scheduler_thread = Thread(target=self.schedule_upload)
        self.scheduler_thread.start()

    def _creacion_componentes(self):
        # Contenedor principal
        contenedor = tk.Frame(self, bg='white')
        contenedor.pack()

        # ===============Primer frame para la imagen=================
        imagen_lateral = tk.Frame(contenedor, width=180, height=500, bg='white', pady=10, padx=5)
        imagen_lateral.grid(row=0, column=0, sticky='n')

        # Cargar la imagen
        ruta_imagen = 'C:/interfaz_netlabsx/logoNetlabsx.png'
        imagen = Image.open(ruta_imagen)
        imagen = imagen.resize((160, 160), Image.BICUBIC)
        img = ImageTk.PhotoImage(imagen)

        # Mostrar la imagen en un Label
        label_imagen = tk.Label(imagen_lateral, image=img, bg='white')
        label_imagen.image = img
        label_imagen.grid(row=0, column=0, columnspan=2)

        # Cargar información
        espacio = tk.Label(imagen_lateral, text='', bg='white', pady=30)
        espacio.grid(row=1, column=0, columnspan=2)

        label_serv = tk.Label(imagen_lateral, text='Datos del servidor\n', bg='white', pady=5)
        label_serv.grid(row=2, column=0, columnspan=2, sticky='w')

        label_ip = tk.Label(imagen_lateral, text='IP:', bg='white')
        label_ip.grid(row=3, column=0, sticky='w')
        ip = tk.Entry(imagen_lateral)
        ip.grid(row=3, column=1)
        ip.insert(0, '192.168.1.97')

        label_puerto = tk.Label(imagen_lateral, text='Puerto:', bg='white', pady=5)
        label_puerto.grid(row=4, column=0, sticky='w')
        puerto = tk.Entry(imagen_lateral)
        puerto.grid(row=4, column=1)
        puerto.insert(0, '1897')

        espacio2 = tk.Label(imagen_lateral, text='', bg='white', pady=10)
        espacio2.grid(row=5, column=0, columnspan=2)

        botonConectar = ttk.Button(imagen_lateral, text='Conectar', width=25, command=self._conectar_servidor)
        botonConectar.grid(row=6, column=0, columnspan=2)

        botonConectar = ttk.Button(imagen_lateral, text='Subir archivo', width=25, command=self.upload_file)
        botonConectar.grid(row=7, column=0, columnspan=2)

        #============== Segundo frame caja de texto=======================
        fcaja_texto = tk.Frame(contenedor, width=420, height=550, bg='white', bd=1, highlightbackground='gray80',
                               highlightthickness=2)
        fcaja_texto.grid(row=0, column=1)

        label_datos = tk.Label(fcaja_texto, text='Datos recibidos desde el equipo:', bg='white',width=55,height=2)
        label_datos.grid(row=0, column=0, sticky='w')

        # Agregar caja de texto que abarque el espacio sobrante
        self.caja_texto = scrolledtext.ScrolledText(fcaja_texto, width=50, height=30, wrap=tk.WORD)
        self.caja_texto.grid(row=1, column=0,
                        sticky='nsew')  # Hacer que la caja de texto se expanda en todas las direcciones

        # ==================Tercer Frame subida de archivo===================
        fsubida = tk.Frame(contenedor, width=600, bg='#DDDDDD')
        fsubida.grid(row=1, column=0, columnspan=2)

        label_archivoe = tk.Label(fsubida, text='Enviando Archivo al sistema Netlabsx:',bg='#DDDDDD', height=4, width=90)
        label_archivoe.grid(row=0, column=0, sticky='w')

        self.barra_progreso = ttk.Progressbar(fsubida, orient='horizontal', length=550,)
        self.barra_progreso.grid(row=1, column=0)
        self.label_archivoc = tk.Label(fsubida, text='Fecha de utima subida:', bg='#DDDDDD', height=1)
        self.label_archivoc.grid(row=2, column=0, sticky='w')


if __name__ == '__main__':
    interfazg = GraficosNet()
    interfazg.mainloop()
