import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from turtle import title
import posting


class Window:
    def __init__(self, root):
        # root.configure(bg='black')
        self.root = root
        self.home_dir = str(Path.home())
        self.reddit = posting.authenticate()

        # self.init_subreddits_list()
        self.init_files_list()
        self.init_title_entry()

    def init_subreddits_list(self):
        subreddits_frame = tk.Frame(self.root, bd='5')
        subreddits_frame.pack()
        subreddits_list = tk.Listbox(subreddits_frame, selectmode='extended', width=54)
        subreddits_list.pack()
        self.subreddits_list = subreddits_list

    def init_files_list(self):
        root = self.root
        files_frame = tk.Frame(root, bd='5')
        files_frame.pack()
        left_frame = tk.Frame(files_frame, bd='5')
        left_frame.pack(side=tk.LEFT)
        right_frame = tk.Frame(files_frame, bd='5')
        right_frame.pack(side=tk.RIGHT)
        label = tk.Label(left_frame, text = 'List of selected Files', justify='left')
        label.pack()
        files_list = tk.Listbox(left_frame, selectmode='extended', width=54)
        files_list.pack()
        self.files_list = files_list

        select_button = ttk.Button(
            right_frame,
            text='Select Files',
            command=self.select_files
        )
        select_button.pack(expand=True)

        remove_button = ttk.Button(
            right_frame,
            text='Remove Selected',
            command=self.remove_selected
        )
        remove_button.pack(expand=True)


    def init_title_entry(self):
        root = self.root
        frame = tk.Frame(root, bd='5')
        frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        left_frame = tk.Frame(frame, bd='5')
        left_frame.pack(side=tk.LEFT)
        label = tk.Label(frame, text = 'Title', justify='left')
        label.pack(side=tk.LEFT, fill=tk.BOTH)
        title_entry = tk.Entry(frame, width = 20)
        title_entry.insert(0,'title')
        title_entry.pack(side=tk.LEFT)
        self.title_entry = title_entry

        frame = tk.Frame(root, bd='5')
        frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        left_frame = tk.Frame(frame, bd='5')
        left_frame.pack(side=tk.LEFT)
        submit_button = ttk.Button(
            left_frame,
            text='Submit Files',
            command=self.submit_files
        )
        submit_button.pack()

    def submit_files(self):
        files = self.files_list.get(0, tk.END)
        print('Submitting:', files)
        showinfo(
            title='Submitting',
            message='Click Ok to confirm'
        )
        post_data = posting.process_files(files, self.title_entry.get(), True)
        posting.post(self.reddit, post_data)
        showinfo(
            title='Done',
            message='The files has been submitted'
        )


    def select_files(self):
        filetypes = (
            ('All files', '*.*'),
            ('text files', '*.txt'),
        )
        filenames = fd.askopenfilenames(
            title='Select files',
            initialdir=os.getcwd(),
            filetypes=filetypes
        )
        for filename in filenames:
            try:
                index = self.files_list.get(0, tk.END).index(filename)
            except:
                self.files_list.insert(tk.END, filename)


    def remove_selected(self):
        selection = self.files_list.curselection()
        if not selection:
            showinfo(message='No selection')
            return
        for index in reversed(selection):
            self.files_list.delete(index)


if __name__ == '__main__':
    # create the root window
    root = tk.Tk()
    root.title('Reddit Publisher')
    # root.resizable(False, False)
    root.geometry('620x420')
    window = Window(root)
    root.mainloop()
