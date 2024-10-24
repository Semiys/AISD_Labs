import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import mimetypes
import threading
import logging
import json
import sys
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

logging.basicConfig(filename='file_sorter.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
def get_file_type(file_path):
    try:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            main_type, sub_type = mime_type.split('/')
            if main_type == 'application':
                if sub_type in ['zip', 'x-rar-compressed', 'x-7z-compressed', 'x-tar', 'gzip']:
                    return 'archive'
                elif sub_type in ['pdf', 'msword', 'vnd.openxmlformats-officedocument.wordprocessingml.document',
                                  'vnd.ms-excel', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                  'vnd.ms-powerpoint', 'vnd.openxmlformats-officedocument.presentationml.presentation']:
                    return 'document'
                elif sub_type in ['x-executable', 'x-sharedlib', 'x-msdos-program', 'x-msdownload']:
                    return 'executable'
            elif main_type == 'text':
                if sub_type in ['plain', 'html', 'css', 'javascript']:
                    return 'text'
                elif sub_type in ['x-python', 'x-java-source', 'x-c++', 'x-csharp']:
                    return 'code'
            elif main_type in ['image', 'audio', 'video']:
                return main_type

        _, extension = os.path.splitext(file_path)
        extension = extension.lower()

        if extension in ['.exe', '.dll', '.bat', '.com', '.msi']:
            return 'executable'
        elif extension in ['.txt', '.log', '.ini', '.cfg']:
            return 'text'
        elif extension in ['.py', '.java', '.cpp', '.h', '.cs', '.js', '.php', '.rb', '.go', '.swift']:
            return 'code'
        elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']:
            return 'image'
        elif extension in ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.wma']:
            return 'audio'
        elif extension in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']:
            return 'video'
        elif extension in ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2']:
            return 'archive'
        elif extension in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp']:
            return 'document'

        return 'other'
    except Exception as e:
        logging.error(f"Ошибка при определении типа файла {file_path}: {str(e)}")
        return 'unknown'

def sort_files(source_folder, destination_folder):
    try:
        total_files = len([f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))])
        processed_files = 0
        sorted_files = {}

        for filename in os.listdir(source_folder):
            file_path = os.path.join(source_folder, filename)
            if os.path.isfile(file_path):
                file_type = get_file_type(file_path)
                category = file_type

                category_folder = os.path.join(destination_folder, category)
                os.makedirs(category_folder, exist_ok=True)

                new_file_path = os.path.join(category_folder, filename)
                shutil.copy2(file_path, new_file_path)

                sorted_files[filename] = {
                    'original_path': file_path,
                    'new_path': new_file_path,
                    'file_type': file_type,
                    'category': category
                }

                os.remove(file_path)

                processed_files += 1
                progress = (processed_files / total_files) * 100
                progress_var.set(progress)
                update_log(f"Обработан файл: {filename}")
                root.update_idletasks()

        report_path = os.path.join(destination_folder, 'sorting_report.json')
        with open(report_path, 'w', encoding='utf-8') as report_file:
            json.dump(sorted_files, report_file, ensure_ascii=False, indent=4)

        messagebox.showinfo("Успех", f"Сортировка файлов завершена! Отчет сохранен в {report_path}")
        logging.info(f"Сортировка завершена. Обработано файлов: {processed_files}")
    except Exception as e:
        logging.error(f"Ошибка при сортировке файлов: {str(e)}")
        messagebox.showerror("Ошибка", f"Произошла ошибка при сортировке файлов: {str(e)}")

root = tk.Tk()
root.title("Интеллектуальный сортировщик файлов")
root.geometry("600x630")
root.resizable(False, False)

def choose_source_folder():
    folder = filedialog.askdirectory()
    if folder:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, folder)

def choose_destination_folder():
    folder = filedialog.askdirectory()
    if folder:
        destination_entry.delete(0, tk.END)
        destination_entry.insert(0, folder)

def start_sorting_thread():
    source = source_entry.get()
    destination = destination_entry.get()
    if source and destination:
        start_button.config(state=tk.DISABLED)
        progress_var.set(0)
        log_text.config(state=tk.NORMAL)
        log_text.delete(1.0, tk.END)
        log_text.config(state=tk.DISABLED)
        threading.Thread(target=sort_files_wrapper, args=(source, destination), daemon=True).start()
    else:
        messagebox.showwarning("Предупреждение",
                               "Пожалуйста, выберите исходную папку и папку назначения.")

def sort_files_wrapper(source, destination):
    try:
        sort_files(source, destination)
    finally:
        start_button.config(state=tk.NORMAL)

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(frame, text="Исходная папка:").grid(column=0, row=0, sticky=tk.W, pady=5)
source_entry = ttk.Entry(frame, width=50)
source_entry.grid(column=0, row=1, sticky=(tk.W, tk.E), pady=5)
ttk.Button(frame, text="Выбрать", command=choose_source_folder).grid(column=1, row=1, sticky=tk.W, padx=5)

ttk.Label(frame, text="Папка назначения:").grid(column=0, row=2, sticky=tk.W, pady=5)
destination_entry = ttk.Entry(frame, width=50)
destination_entry.grid(column=0, row=3, sticky=(tk.W, tk.E), pady=5)
ttk.Button(frame, text="Выбрать", command=choose_destination_folder).grid(column=1, row=3, sticky=tk.W, padx=5)

start_button = ttk.Button(frame, text="Начать сортировку", command=start_sorting_thread)
start_button.grid(column=0, row=4, columnspan=2, pady=20)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(frame, variable=progress_var, maximum=100)
progress_bar.grid(column=0, row=5, columnspan=2, sticky=(tk.W, tk.E), pady=10)

log_text = tk.Text(frame, height=15, width=70, wrap=tk.WORD)
log_text.grid(column=0, row=6, columnspan=2, sticky=(tk.W, tk.E), pady=10)
log_text.config(state=tk.DISABLED)

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=log_text.yview)
scrollbar.grid(column=2, row=6, sticky=(tk.N, tk.S))
log_text.configure(yscrollcommand=scrollbar.set)

def update_log(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)

class TextHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        update_log(msg)

text_handler = TextHandler()
text_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(text_handler)

def clear_logs():
    log_text.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)
    log_text.config(state=tk.DISABLED)

def open_report_folder():
    destination = destination_entry.get()
    if destination:
        os.startfile(destination)
    else:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите папку назначения.")

def on_closing():
    if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
        root.destroy()

button_frame = ttk.Frame(frame)
button_frame.grid(column=0, row=7, columnspan=2, pady=10)

clear_button = ttk.Button(button_frame, text="Очистить логи", command=clear_logs)
clear_button.grid(column=0, row=0, padx=5)

report_button = ttk.Button(button_frame, text="Открыть папку с отчетом", command=open_report_folder)
report_button.grid(column=1, row=0, padx=5)

exit_button = ttk.Button(button_frame, text="Выход", command=on_closing)
exit_button.grid(column=2, row=0, padx=5)

root.protocol("WM_DELETE_WINDOW", on_closing)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Открыть исходную папку", command=choose_source_folder)
file_menu.add_command(label="Открыть папку назначения", command=choose_destination_folder)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=on_closing)

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Справка", menu=help_menu)
help_menu.add_command(label="О программе", command=lambda: messagebox.showinfo("О программе",
                                                                               "Интеллектуальный сортировщик файлов\nВерсия 1.0"))

def save_settings():
    settings = {
        "source_folder": source_entry.get(),
        "destination_folder": destination_entry.get()
    }
    with open("settings.json", "w") as f:
        json.dump(settings, f)

def load_settings():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
        source_entry.insert(0, settings.get("source_folder", ""))
        destination_entry.insert(0, settings.get("destination_folder", ""))
    except FileNotFoundError:
        pass

load_settings()

root.protocol("WM_DELETE_WINDOW", lambda: [save_settings(), on_closing()])

custom_rules = {}

root.mainloop()
