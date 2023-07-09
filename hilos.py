import threading

from listener_archivo import FileSizeWatcher
from servidorLIS import ServidorLIS


class ServidorLISThread(threading.Thread):
    def run(self):
        server_ip = '192.168.1.97'
        server_port = 7118

        servidor = ServidorLIS(server_ip, server_port)
        servidor.iniciar_servidor()

class FileWatcherThread(threading.Thread):
    def run(self):
        file_watcher = FileSizeWatcher("C:\\interfaz_netlabsx\\listener.txt")
        file_watcher.watch()
