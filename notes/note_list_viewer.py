from database.notes_database_action import NotesDatabaseAction
from lib_imports import (PALETTE, Canvas, Combobox, Frame, Label,
                         Optional, Scrollbar, messagebox, textwrap)
from notes.note_information import NoteInformation


class NoteListViewer:
    """
    A class that represents a note list viewer.
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create and return a new instance of the NoteListViewer class,
        or return an existing instance if one already exists.
        """
        if cls.__instance is None:
            cls.__instance = super(NoteListViewer, cls).__new__(cls)
        return cls.__instance

    def __init__(self, main_window, operation_buttons_window, operation_object, side_object):
        """
        Initializes the OperationButtonManager class.

        Args:
            main_window (tkinter.Frame): The main application frame in the window.
            operation_buttons_window (tkinter.Frame): The frame for the operation buttons
                                              in the application window.
            operation_object (object): The object of the OperationButtonManager class.
        """
        self.main_frame = main_window
        self.operation_buttons_frame = operation_buttons_window
        self.operation_object = operation_object
        self.side_object = side_object
        self.complete_note_info = NoteInformation(
            self.main_frame, self.operation_buttons_frame, self.side_object)
        self.note_sorting = "newest"
        self.frame_to_display = None
        self.current_note_category = None

    def create_note_display_interface(self, note_category: Optional[str] = "All notes"):
        """
        Creates the note display interface.

        Args:
            note_category (Optional[str]): The category of notes to display.
            Defaults to "All notes".
        """
        self.current_note_category = note_category
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create an area to display notes
        notes_display_frame = Frame(self.main_frame, bg=PALETTE["main"]["3color"])
        notes_display_frame.grid(row=0, column=0, padx=5, pady=10)

        self.combobox(notes_display_frame)

        notes_canvas = Canvas(notes_display_frame, width=775, height=525)
        scrollbar_for_notes_canvas = Scrollbar(
            notes_display_frame, orient="vertical", command=notes_canvas.yview)

        notes_canvas.configure(
            yscrollcommand=scrollbar_for_notes_canvas.set,
            bg=PALETTE["main"]["3color"],
            borderwidth=0,
            highlightthickness=0)
        notes_canvas.pack(side="left", fill="both", expand=True, pady=1)

        all_database_notes = self.select_all_database_notes(scrollbar_for_notes_canvas)

        self.note_display(notes_canvas, all_database_notes)

    def combobox(self, notes_display_frame: Frame):
        """
       Creates a combobox widget to select the sorting option for notes.

       Args:
           notes_display_frame (tkinter.Frame): The frame to which the combobox will be added.
       """
        sorting_values = [
            "by creation date (newest)",
            "by creation date (oldest)",
            "by name (A to Z)",
            "by name (Z to A)",
        ]

        combo_sort = Combobox(
            notes_display_frame,
            values=sorting_values,
            background=PALETTE["main"]["3color"],
            state="readonly",
        )

        mapping = {
            "newest": 0,
            "oldest": 1,
            "atoz": 2,
            "ztoa": 3,
        }

        combo_sort.bind(
            "<<ComboboxSelected>>",
            lambda event: self._handle_combobox(combo_sort, mapping))

        if self.note_sorting in mapping:
            combo_sort.current(mapping[self.note_sorting])

        combo_sort.pack(padx=5)

    def _handle_combobox(self, combo: Combobox, mapping: dict):
        """
        Handles the event when a sorting option is selected from the combobox.

        Args:
            combo (tkinterCombobox): The combobox widget.
            mapping (dict): A dictionary mapping sorting options
            to their corresponding index values.
        """
        selected = combo.current()

        if selected in mapping.values():
            self.note_sorting = next(
                key for key, value in mapping.items() if value == selected)
            self.create_note_display_interface(note_category=self.current_note_category)

    def select_all_database_notes(self, scrollbar_for_notes_canvas: Scrollbar):
        """
        Retrieves all database notes based on the current note category and sorting option.

        Args:
            scrollbar_for_notes_canvas(tkinter.Scrollbar): The scrollbar widget
            for the notes canvas.

        Returns:
            list: A list of all the database notes.
        """
        all_database_notes = NotesDatabaseAction.select_all_notes(
            table_name="notes_info",
            category=self.current_note_category,
            sorting=self.note_sorting)

        if len(all_database_notes) > 5:
            scrollbar_for_notes_canvas.pack(side="right", fill="y")

        return all_database_notes

    def note_display(self, notes_canvas: Canvas, all_database_notes: list):
        """
        Displays the notes on the canvas.

        Args:
            notes_canvas(tkinter.Canvas): The canvas widget to display the notes.
            all_database_notes (list): A list of all the database notes to be displayed.
        """
        # Create a frame to display data on canvas
        self.frame_to_display = Frame(notes_canvas, bg=PALETTE["main"]["3color"])

        self.frame_to_display.bind(
            "<Configure>",
            lambda e: notes_canvas.configure(scrollregion=notes_canvas.bbox("all")))

        notes_canvas.create_window((0, 0), window=self.frame_to_display, anchor="nw")

        # Write out all the data in the frame
        for note_num in range(len(all_database_notes)):
            note_label = Label(self.frame_to_display)
            note_label.configure(bg=PALETTE["main"]["3color"])

            self.create_all_elements_in_frame(note_label, all_database_notes, note_num)

            note_label.pack(anchor="nw")

    def create_all_elements_in_frame(
            self, note_frame: Label, all_database_notes: list, note_num: int):
        """
        Creates all the elements within a note frame.

        Args:
            note_frame(tkinter.Label): The Label to which the elements will be added.
            all_database_notes (list): A list of all the database notes.
            note_num (int): The index of the current note being processed.
        """
        all_note_data = []
        Label(note_frame, text=f"{all_database_notes[note_num]['id']}")

        category_label = Label(
            note_frame,
            text=f"{all_database_notes[note_num]['note_category']}",
            font=("Arial bold", 13),
            bg=PALETTE["secondary"]["1color"],
            fg=PALETTE["main"]["3color"],
            anchor="nw",
        )

        datetime_label = Label(
            note_frame,
            text=f"{str(all_database_notes[note_num]['created_at'])[:10]}",
            font=("Arial bold", 13),
            bg=PALETTE["secondary"]["1color"],
            fg=PALETTE["main"]["3color"],
            anchor="nw",
        )

        # Second row with title
        title_label = Label(
            note_frame,
            text=textwrap.shorten(
                all_database_notes[note_num]["note_name"], width=70, placeholder="..."
            ),
            font=("Arial", 16, "bold"),
            bg=PALETTE["main"]["3color"],
            fg="white",
            anchor="nw",
        )

        # Third row with description
        description_label = Label(
            note_frame,
            text=textwrap.shorten(
                all_database_notes[note_num]["note_description"],
                width=130,
                placeholder="...",
            ),
            bg=PALETTE["main"]["3color"],
            font=("Arial", 12),
            anchor="nw",
        )

        empty_cell = Frame(
            note_frame, width=765, height=2, bg=PALETTE["main"]["1color"]
        )

        category_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        datetime_label.grid(row=0, column=1, sticky="e", padx=2, pady=2)
        title_label.grid(row=1, column=0, columnspan=2, padx=10, pady=0, sticky="w")
        description_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        empty_cell.grid(row=3, column=0, columnspan=2, pady=5, sticky="news")

        all_note_data.append(note_frame)

        for place in (note_frame, title_label, description_label):
            place.bind(
                "<Button-1>",
                lambda event, labels=tuple(all_note_data),
                       active_id=all_database_notes[note_num]["id"]:
                self._change_active_data_color(labels, active_id))

            place.bind(
                "<Double-Button-1>",
                lambda event, active_note=note_frame: self.complete_note_info.open_note_information(
                    active_note.winfo_children()[0].cget("text")))

    def _change_active_data_color(self, labels_list: list, active_id: int):
        """
        Changes the color of the active note and its labels.

        Args:
            labels_list (list): A list of labels belonging to the active note.
            active_id (int): The ID of the active note.
        """
        self.operation_object.add_dynamic_buttons(active_id, self.current_note_category)

        # Go around all the data on frame and change the color of all but the current one
        for child in self.frame_to_display.winfo_children():
            if isinstance(child, Label):
                is_active = (
                                    child.cget("bg") == PALETTE["main"]["3color"]
                                    and child in labels_list
                            ) or (
                                    child.cget("bg") == PALETTE["main"]["1color"]
                                    and child in labels_list
                            )

                for label in child.winfo_children()[3:-1]:
                    label.config(
                        bg=PALETTE["main"]["1color"]
                        if is_active
                        else PALETTE["main"]["3color"]
                    )

                child.config(
                    bg=PALETTE["main"]["1color"]
                    if is_active
                    else PALETTE["main"]["3color"]
                )
