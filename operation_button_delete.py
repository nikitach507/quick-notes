import tkinter
from tkinter import *
from tkinter import messagebox

from main import *
from database.notes_database_action import *


class OperationButtonDelete:
    def __init__(self, root):
        self.root = root
        self.label = None

    @staticmethod
    def delete_note_button(current_id, object):
        answer = messagebox.askokcancel("Delete Note", "Are you sure you want to delete the note?")
        if answer:
            NotesDatabaseAction.delete_note("notes_info", note_id=current_id)
        object.note_display_interface()

    def open_new_window(self, current_label):
        new_window = Toplevel(self.root)
        # new_window.title(f"{current_label[4].cget('text')}")
        new_window.geometry("420x170")
        new_window.minsize(420, 140)
        new_window.configure(bg="#787D46")

        frame = Frame(new_window)
        frame.configure(bd=4, highlightbackground="white", highlightthickness=2)
        frame.pack(expand=True)
        # new_window.bind("<Configure>", resize_frame)
        for i in current_label.winfo_children()[:-1]:
            self.label = Label(frame, text=f"{i.cget('text')}", justify="center",
                               border=3, highlightbackground="#787D46", wraplength=400)
            self.label.pack(expand=True)

            canvas = Canvas(frame, height=1, width=400, bg="white", )
            canvas.pack()

            # Добавление горизонтальной линии
            canvas.create_line(0, 2, 300, 2)
            canvas.configure()
