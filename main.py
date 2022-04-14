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

        self.init_subreddits_list()
        self.init_files_list()
        self.init_title_entry()

    def init_subreddits_list(self):
        root = self.root
        label_frame = tk.Frame(root, bd='5')
        label_frame.pack(anchor=tk.NW)
        label = tk.Label(label_frame, text = 'List of Subreddits')
        label.pack()

        actions_frame = tk.Frame(root, bd='5')
        actions_frame.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)
        subreddit_entry = tk.Entry(actions_frame, width = 20)
        subreddit_entry.pack(side=tk.LEFT)
        self.subreddit_entry = subreddit_entry
        select_button = ttk.Button(
            actions_frame,
            text='Add Subreddit',
            command=self.add_subreddit_entry
        )
        select_button.pack(side=tk.LEFT)
        remove_button = ttk.Button(
            actions_frame,
            text='Remove Selected',
            command=self.remove_selected_subreddits
        )
        remove_button.pack(side=tk.LEFT)

        subreddits_frame = tk.Frame(self.root, bd='5', relief=tk.RAISED, borderwidth=1)
        subreddits_frame.pack()
        subreddits_list = tk.Listbox(subreddits_frame, selectmode='extended', width=54)
        subreddits_list.pack()
        self.subreddits_list = subreddits_list
        self.load_initial_subreddits()

    def load_initial_subreddits(self):
        if posting.subreddits:
            for value in posting.subreddits:
                self.subreddits_list.insert(tk.END, value)

    def init_files_list(self):
        root = self.root
        label_frame = tk.Frame(root, bd='5')
        label_frame.pack(anchor=tk.NW)
        label = tk.Label(label_frame, text = 'List of Files')
        label.pack()

        actions_frame = tk.Frame(root, bd='5')
        actions_frame.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)
        select_button = ttk.Button(
            actions_frame,
            text='Pick Files',
            command=self.select_files
        )
        select_button.pack(side=tk.LEFT)
        remove_button = ttk.Button(
            actions_frame,
            text='Remove Selected',
            command=self.remove_selected_files
        )
        remove_button.pack(side=tk.LEFT)

        files_frame = tk.Frame(root, bd='5', relief=tk.RAISED, borderwidth=1)
        files_frame.pack()
        files_list = tk.Listbox(files_frame, selectmode='extended', width=54)
        files_list.pack()
        self.files_list = files_list

    def init_title_entry(self):
        root = self.root
        frame = tk.Frame(root, bd='5')
        frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        label = tk.Label(frame, text = 'Title')
        label.pack(side=tk.LEFT, fill=tk.BOTH)
        title_entry = tk.Entry(frame, width = 20)
        title_entry.insert(0, 'some title')
        title_entry.pack(side=tk.LEFT)
        self.title_entry = title_entry

        frame = tk.Frame(root, bd='5')
        frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.nsfw_var = tk.IntVar()
        nsfw_check = tk.Checkbutton(frame, text="NFSW", variable=self.nsfw_var)
        nsfw_check.pack(padx = 5, pady = 5, expand=True)

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

    def add_subreddit_entry(self):
        value = self.subreddit_entry.get()
        try:
            self.subreddits_list.get(0, tk.END).index(value)
        except:
            self.subreddits_list.insert(tk.END, value)
        finally:
            self.subreddit_entry.delete(0, tk.END)
            self.subreddit_entry.focus_set()

    def remove_selected_subreddits(self):
        selection = self.subreddits_list.curselection()
        if not selection:
            showinfo(message='No selection')
            return
        for index in reversed(selection):
            self.subreddits_list.delete(index)

    def submit_files(self):
        files = self.files_list.get(0, tk.END)
        subreddits = self.subreddits_list.get(0, tk.END)
        print('Submitting:', files)
        showinfo(
            title='Submitting',
            message='Click Ok to confirm'
        )
        post_data = posting.process_files(files, self.title_entry.get(), True)
        nsfw = bool(self.nsfw_var.get())
        posting.post(self.reddit, post_data, subreddits, nsfw=nsfw)
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
                self.files_list.get(0, tk.END).index(filename)
            except:
                self.files_list.insert(tk.END, filename)

    def remove_selected_files(self):
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
    root.geometry('')
    window = Window(root)
    root.mainloop()
