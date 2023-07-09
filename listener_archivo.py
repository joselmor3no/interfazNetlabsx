import os
import shutil
import time

class FileSizeWatcher:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_size = self.get_file_size()

    def get_file_size(self):
        return os.path.getsize(self.file_path)

    def watch(self):
        while True:
            # Esperar un intervalo de tiempo
            time.sleep(1)

            # Obtener el tamaño actual del archivo
            current_size = self.get_file_size()

            # Verificar si el tamaño ha cambiado
            if current_size != self.file_size:
                print(f"El archivo '{self.file_path}' cambió de tamaño a {current_size} bytes.")
                self.file_size = current_size
                # Esperar 30 segundos
                time.sleep(30)
                # Hacer una copia del archivo
                file_name, file_ext = os.path.splitext(self.file_path)
                backup_path = f"C:\\interfaz_netlabsx\\sucursal139qui{file_ext}"
                shutil.copy2(self.file_path, backup_path)
                print(f"Se hizo una copia del archivo en '{backup_path}'.")


# Ejemplo de uso
if __name__ == "__main__":
    file_watcher = FileSizeWatcher("C:\\interfaz_netlabsx\\listener.txt")
    #file_watcher.watch()
