from database.notes_database_action import NotesDatabaseAction
from lib_imports import PALETTE, Frame, Label, Text, Toplevel


class NoteDisplayWindow:
    """
    A class for displaying information about the selected note in a new window.
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create and return a new instance of the NoteDisplayWindow class,
        or return an existing instance if one already exists.
        """
        if cls.__instance is None:
            cls.__instance = super(NoteDisplayWindow, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.label = None

    def create_new_window(self, note_id: int):
        """
        Initializes a new window for the note.

        Args:
            note_id (int): The id of the note to display.
        """
        info_note = NotesDatabaseAction.select_note("notes_info", note_id)
        note_window = Toplevel()
        note_window.title(f"{info_note[0]['note_name']}")
        note_window_width, note_window_height = 415, 275
        note_window.geometry(f"{note_window_width}x{note_window_height}")
        note_window.minsize(note_window_width, note_window_height)
        note_window.configure(bg=PALETTE["main"]["1color"])
        note_window.grid_rowconfigure(0, weight=1)
        note_window.grid_columnconfigure(0, weight=1)

        self.add_info_about_note(note_window, info_note)

    def add_info_about_note(self, note_window: Toplevel, info_note: dict):
        """
        Adds information about the note to the note_window.

        Args:
            note_window (Toplevel): The window where the information will be displayed.
            info_note (dict): The dictionary containing the information about the note.
        """
        information_frame = Frame(note_window)
        information_frame.configure(
            bd=4,
            highlightthickness=1,
            highlightcolor=PALETTE["main"]["3color"],
            bg=PALETTE["main"]["3color"])
        information_frame.pack(expand=True)

        information_frame.grid(row=0, column=0, sticky="nsew")
        information_frame.grid_rowconfigure(2, weight=1)
        information_frame.grid_columnconfigure(0, weight=1)

        self._draw_name_note_area(information_frame, info_note)

        self._draw_date_category_note_area(information_frame, info_note)

        self._draw_description_note_area(information_frame, info_note)

    @staticmethod
    def _draw_name_note_area(info_frame: Frame, info_note: dict):
        """
        Draws the name section of the note in the info_frame.

        Args:
            info_frame (tkinter.Frame): The frame where the information will be displayed.
            info_note (dict): The dictionary containing the information about the note.
        """
        name = info_note[0]["note_name"]
        name_label = Text(
            info_frame,
            height=3, width=43,
            wrap="word",
            font=("Arial", 16, "bold"),
            bg=PALETTE["main"]["3color"],
            highlightthickness=0,
            padx=5, pady=5)

        name_label.insert("insert", name)
        name_label.configure(state="disabled")
        name_label.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def _draw_date_category_note_area(info_frame: Frame, info_note: dict):
        """
        Draws the date and category section of the note in the info_frame.

        Args:
            info_frame (tkinter.Frame): The frame where the information will be displayed.
            info_note (dict): The dictionary containing the information about the note.
        """
        category = info_note[0]["note_category"]
        date = info_note[0]["created_at"]
        date_label = Label(
            info_frame,
            text=f"{category} | {date}",
            justify="center",
            font=("Arial", 12, "bold"),
            bg=PALETTE["secondary"]["1color"],
            fg=PALETTE["main"]["2color"],
            border=0,
            wraplength=400,
            pady=3)
        date_label.grid(row=1, column=0, sticky="nsew", pady=10, padx=4)

    @staticmethod
    def _draw_description_note_area(info_frame: Frame, info_note: dict):
        """
        Draws the description section of the note in the info_frame.

        Args:
            info_frame (tkinter.Frame): The frame where the information will be displayed.
            info_note (dict): The dictionary containing the information about the note.
        """
        description = info_note[0]["note_description"]
        description_label = Text(
            info_frame,
            height=10, width=49,
            wrap="word",
            font="Arial",
            bg=PALETTE["main"]["3color"],
            highlightthickness=0,
            padx=5, pady=5)

        description_label.insert("insert", description)
        description_label.configure(state="disabled")
        description_label.grid(row=2, column=0, sticky="nsew")
