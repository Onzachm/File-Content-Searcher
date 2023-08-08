import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, simpledialog, messagebox
import threading
import queue
import datetime

def contains_keyword(file_path, keyword):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            return keyword in content
    except Exception:
        return False

def search_directory(directory, keyword, progress_queue):
    total_files = sum([len(files) for _, _, files in os.walk(directory)])
    checked_files = 0

    matches = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if contains_keyword(file_path, keyword):
                matches.append(file_path)

            checked_files += 1
            progress_ratio = checked_files / total_files
            progress_queue.put(progress_ratio)

    progress_queue.put((checked_files, matches))

def on_search_click():
    directory_to_search = directory_entry.get()
    keyword_to_search = keyword_entry.get().strip()

    if not keyword_to_search:
        result_text.insert(tk.END, "Please specify a keyword to search for.\n")
        return

    if not os.path.isdir(directory_to_search):
        result_text.insert(tk.END, f"'{directory_to_search}' is not a valid directory path.\n")
        return

    result_text.delete(1.0, tk.END)
    progress_bar["value"] = 0
    root.update()

    # Start the search in a separate thread
    progress_queue = queue.Queue()
    search_thread = threading.Thread(target=search_directory, args=(directory_to_search, keyword_to_search, progress_queue))
    search_thread.start()

    # Check the progress periodically and update the GUI
    root.after(100, lambda: check_progress(progress_queue, keyword_to_search))

def check_progress(progress_queue, keyword):
    try:
        while True:
            item = progress_queue.get_nowait()
            if isinstance(item, float):
                progress_bar["value"] = item * 100
            elif isinstance(item, tuple):  # The search is done
                files_scanned, matching_files = item
                if matching_files:
                    result_text.insert(tk.END, f"Files containing '{keyword}' in their contents:\n")
                    for file in matching_files:
                        result_text.insert(tk.END, f"{file}\n")
                else:
                    result_text.insert(tk.END, f"No files containing '{keyword}' were found in the specified directory.\n")
                save_log(files_scanned, matching_files, keyword)
                return  # Exit the function and stop checking for updates
    except queue.Empty:
        pass
    root.after(100, lambda: check_progress(progress_queue, keyword))

def save_log(files_scanned, matching_files, keyword):
    log_content = []
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_content.append(f"Search performed on: {current_time}\n")
    log_content.append(f"Keyword searched for: '{keyword}'\n")
    log_content.append(f"Total files scanned: {files_scanned}\n")
    log_content.append(f"Total matches found: {len(matching_files)}\n")
    log_content.append("-" * 40 + "\n")
    for file in matching_files:
        log_content.append(file + "\n")
    
    save_path = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log files", "*.log"), ("All files", "*.*")])
    if save_path:
        with open(save_path, "w", encoding="utf-8") as log_file:
            log_file.writelines(log_content)
        messagebox.showinfo("Info", "Log file saved successfully!")

def browse_directory():
    folder_selected = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, folder_selected)

# Create the main window
root = tk.Tk()
root.title("File Content Searcher")

# Create and place widgets
directory_label = tk.Label(root, text="Directory to search:")
directory_label.pack(padx=10, pady=5)

directory_entry = tk.Entry(root, width=50)
directory_entry.pack(padx=10, pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.pack(padx=10, pady=5)

keyword_label = tk.Label(root, text="Keyword to search for:")
keyword_label.pack(padx=10, pady=5)

keyword_entry = tk.Entry(root, width=50)
keyword_entry.pack(padx=10, pady=5)

search_button = tk.Button(root, text="Search", command=on_search_click)
search_button.pack(padx=10, pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress_bar.pack(pady=10)

result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.pack(padx=10, pady=5)

# Run the app
root.mainloop()
