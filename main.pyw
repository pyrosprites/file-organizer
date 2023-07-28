import time
import logging
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

username = os.getlogin()
source_dir = f"C:/Users/{username}/Downloads"

def create_folders(base_dir, folders):
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder}' created at '{folder_path}'")
        else:
            print(f"Folder '{folder}' already exists at '{folder_path}'")

class eventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.created_files = []
        self.modified_files = []
        self.moved_files = []
        self.deleted_files = []
        self.moved_back_files = set()

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            print(f"File created: {file_path}")
            self.created_files.append(file_path)

    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            print(f"File modified: {file_path}")
            self.modified_files.append(file_path)

    def on_moved(self, event):
        if not event.is_directory:
            src_path = event.src_path
            dest_path = event.dest_path
            print(f"File moved: {src_path} to {dest_path}")
            self.moved_files.append((src_path, dest_path))

    def on_deleted(self, event):
        if not event.is_directory:
            file_path = event.src_path
            print(f"File deleted: {file_path}")
            self.deleted_files.append(file_path)

    def file_exists_in_directory(self, file_path):
        return os.path.exists(file_path)

    def file_move_criminal(self, file_path, dest_folder, suffix_num=1):
        filename, ext = os.path.splitext(os.path.basename(file_path))
        ext = ext.lower()

        dest_path = os.path.join(source_dir, dest_folder, f"{filename}{ext}")

        while os.path.exists(dest_path):
            dest_path = os.path.join(source_dir, dest_folder, f"{filename}_{suffix_num}{ext}")
            suffix_num += 1

        try:
            shutil.move(file_path, dest_path)
            print(f"File '{os.path.basename(file_path)}' moved to '{dest_folder}' as '{os.path.basename(dest_path)}'")
            self.moved_back_files.add(dest_path)
        except Exception as e:
            print(f"Error moving file '{os.path.basename(file_path)}': {str(e)}")

    def organize_files(self):
        for file_path in self.created_files + self.modified_files + [src_path for src_path, dest_path in self.moved_files]:
            if not os.path.exists(file_path):
                continue

            if file_path in self.moved_back_files:
                if not self.file_exists_in_directory(file_path):
                    self.moved_back_files.remove(file_path)
                continue
            
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()

            dest_folder = "Misc"
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                dest_folder = "Images"
            elif ext in ['.exe', '.msi', '.apk', '.app', '.dmp', '.deb', '.rpm', '.jar', '.appimage', '.snap', '.bat', '.sh', '.com', '.ipa', '.vbs', '.py', '.php', '.html', '.css', '.js', '.json']:
                dest_folder = "Apps and Games"
            elif ext in ['.ttf', '.otf', '.woff', '.woff2', '.eot', '.svg', '.dfont', '.pfa', '.pfb', '.afm', '.ttc']:
                dest_folder = "Projects"
            elif ext in ['.ai', '.psd', '.indd', '.xd', '.aep', '.cdr', 'cmx', '.dwg', '.dxf', '.aseprite', '.clip', '.sketch', '.sai', '.kra', '.afdesign']:
                dest_folder = "Drawings"
            elif ext in ['.tmp']:
                dest_folder = "Temp"

            dest_path = os.path.join(source_dir, dest_folder)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

            _, src_filename = os.path.split(file_path)
            dest_file_path = os.path.join(dest_path, src_filename)
            if not os.path.exists(dest_file_path):
                self.file_move_criminal(file_path, dest_folder)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    file_categories = [
        'Apps and Games',
        'Images',
        'Projects',
        'Drawings',
        'Temp',
        'Misc'
    ]
    
    create_folders(source_dir, file_categories)

    path = source_dir
    event_handler = eventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            event_handler.organize_files()

            event_handler.created_files = []
            event_handler.modified_files = []
            event_handler.moved_files = []

            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

