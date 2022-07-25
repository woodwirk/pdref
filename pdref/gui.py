import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from crawl import crawl

class MessageRedirector(object):
    def __init__(self, text_output):
        self.output = text_output
    
    def write(self, string):
        self.output.configure(state = 'normal')
        self.output.insert(tk.END, string)
        self.output.configure(state = 'disabled')
        self.output.see('end')

    def flush(self):
        pass

def show_output():
    if (root.winfo_height() < 250):
        w = root.winfo_width()
        h = 400
        root.geometry(f'{w}x{h}')

def select_folder(entry):
    folder_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder_path)

def run():
    # Check file input
    refs_path = entry_refs.get()
    notes_path = entry_notes.get()
    earliest_modified_date = entry_date.get()

    if (not refs_path):
        msg = 'Note:\n Please select a folder to look for references'
        print(msg)
        show_output()
        return
    elif (not notes_path):
        msg = 'Note:\n Please set an output folder'
        print(msg)
        show_output()
        return
    else:
        # Run
        bar_status.config(text = "Running...")
        root.update()
        crawl(pdfs_path=refs_path, notes_path=notes_path, earliest_modified_date=earliest_modified_date)
        bar_status.config(text = "Done!")
        show_output()
        return

if __name__ == '__main__':
    # Set up window
    root = tk.Tk()
    root.title('pdref')
    root.geometry('300x210+200+200')
    root.minsize(200, 160)
    root.columnconfigure(0,weight=1)
    
    # Set frames for layout
    frame_paths = tk.Frame(root)
    frame_paths.grid(sticky = tk.EW)
    frame_paths.columnconfigure(1, weight=1)

    # frame_date = tk.Frame(root)
    # frame_date.grid(sticky=tk.EW)
    # frame_date.columnconfigure(1, weight=1)

    frame_run = tk.Frame(root)
    frame_run.grid(sticky=tk.EW)
    frame_run.columnconfigure(0, weight=1)

    frame_stdout = tk.Frame(root)
    frame_stdout.grid(sticky=tk.NSEW)
    frame_stdout.columnconfigure(0, weight=1)
    frame_stdout.rowconfigure(0,weight=1)
    root.rowconfigure(2, weight=1)

    frame_info = tk.Frame(root)
    frame_info.grid(sticky=(tk.S, tk.EW))
    frame_info.columnconfigure(0, weight=1)


    # Path input fields
    button_refs = tk.Button(frame_paths, text = 'Refs Folder', command = lambda:select_folder(entry_refs))
    button_refs.grid(row = 0, column = 0, padx=5, pady=5, sticky=tk.EW)
    entry_refs = tk.Entry(frame_paths)
    entry_refs.grid(row=0, column=1, padx = 5, pady=5, sticky=tk.EW)

    button_notes = tk.Button(frame_paths, text = 'Notes Folder', command = lambda:select_folder(entry_notes))
    entry_notes = tk.Entry(frame_paths)
    button_notes.grid(row = 1, column = 0, padx=5, pady=5, sticky=tk.EW)
    entry_notes.grid(row=1, column=1, padx = 5, pady=5, sticky=tk.EW)

    label_date = tk.Label(frame_paths, text = "Notes since:")
    label_date.grid(row = 2, column = 0, padx=5, pady=5, sticky=tk.EW)
    label_date = tk.Label(frame_paths, text = "Format: YYYY-MM-DD")
    label_date.grid(row = 3, column = 1, sticky=tk.EW)
    entry_date = tk.Entry(frame_paths)
    entry_date.grid(row=2, column=1, padx = 5, pady=5, sticky=tk.EW)

    # Run options
    button_run = tk.Button(frame_run, text = 'Run', command = run, padx=10, pady=10)
    button_run.grid(column=0, row = 0, padx=10, pady=10, sticky=tk.EW)

    # Configure stdout scroll view
    scrolledtext_console = scrolledtext.ScrolledText(frame_stdout, height = 1)
    scrolledtext_console.grid(padx=5, pady=5, sticky=tk.NSEW)
    sys.stdout = MessageRedirector(scrolledtext_console)

    # Bottom info
    bar_status = tk.Label(frame_info, text=(f"pdref v0.1.0"), bd=1, relief=tk.SUNKEN, anchor='w')
    bar_status.grid(sticky=(tk.S, tk.EW))

    # Run GUI
    root.mainloop()