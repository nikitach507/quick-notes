from database.notes_database_action import NotesDatabaseAction
from lib_imports import PALETTE, Button, Canvas, Frame, Label, Text, Set
from notes.note_data_saver import NoteDataSaver


class NoteInformation:
    """
    Represents a note information window.
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create and return a new instance of the NoteInformation class,
        or return an existing instance if one already exists.
        """
        if cls.__instance is None:
            cls.__instance = super(NoteInformation, cls).__new__(cls)
        return cls.__instance

    def __init__(self, main_window, operation_buttons_window, side_object):
        """
        Initializes the OperationButtonManager class.

        Args:
            main_window (tkinter.Frame): The main application frame in the window.
            operation_buttons_window (tkinter.Frame): The frame for the operation buttons
                                              in the application window.
        """
        self.operation_buttons_frame = operation_buttons_window
        self.main_frame = main_window
        self.side_object = side_object
        self.nested_data = {}
        self.name_text_area = None
        self.data_note_frame = None
        self.info_note = None
        self.desc_text_area = None
        self.update_button = None

    def open_note_information(self, note_id: int):
        """
        Opens the information of a note by clearing the interface,
        retrieving the note from the database,
        and drawing the data, supplementary information, triangle of changes, and update button.

        Args:
            note_id (int): The ID of the note to open.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.info_note = NotesDatabaseAction.select_note("notes_info", note_id)

        self._draw_data_note()

        self._draw_supplementary_info_note()

        previous_actions: Set[str] = set()

        self._create_triangle_of_changes(previous_actions)

        self._draw_update_button(note_id)

    def _draw_data_note(self):
        """
        Draws the data section of the note, including the note name and description text areas.
        """
        self.data_note_frame = Frame(
            self.main_frame,
            bg=PALETTE["main"]["1color"],
            highlightbackground=PALETTE["main"]["1color"],
            highlightthickness=2,
            relief="flat",
            highlightcolor=PALETTE["main"]["1color"],
        )
        self.data_note_frame.pack(side="left", padx=5, pady=5, anchor="nw")

        self.name_text_area = Text(
            self.data_note_frame,
            height=3, width=43,
            relief="flat", highlightthickness=0,
            undo=True, wrap="word",
            bg=PALETTE["main"]["3color"],
            font=("Arial", 24, "bold"),
            fg=PALETTE["text"]["1color"],
            padx=10, pady=5,
        )

        self.name_text_area.insert("insert", self.info_note[0]["note_name"])
        self.name_text_area.pack(anchor="nw")

        self.desc_text_area = Text(
            self.data_note_frame,
            height=19, width=67,
            wrap="word", undo=True,
            font=("Arial", 16),
            bg=PALETTE["main"]["3color"],
            highlightthickness=0,
            tabs=15, tabstyle="tabular",
            takefocus=False, spacing1=5,
            padx=10, pady=5,
        )
        self.desc_text_area.insert("insert", self.info_note[0]["note_description"])
        self.desc_text_area.pack(pady=4, anchor="nw")

        self.nested_data["note_name"] = self.name_text_area
        self.nested_data["note_description"] = self.desc_text_area

    def _draw_supplementary_info_note(self):
        """
        Draws the supplementary information section of the note,
        including category, date of addition, and time of addition.
        """
        supplementary_frame = Frame(
            self.main_frame,
            bg=PALETTE["main"]["3color"],
            highlightthickness=0,
            relief="flat",
        )
        supplementary_frame.pack(side="right", expand=True, padx=2, pady=5, anchor="nw")

        back_comm = lambda: self.side_object.create_side_category_list(self.info_note[0]["note_category"])
        Button(supplementary_frame, text="Back",
               bg=PALETTE["secondary"]["1color"],
               fg=PALETTE["text"]["1color"],
               activebackground=PALETTE["secondary"]["1color"],
               activeforeground=PALETTE["text"]["2color"],
               command=back_comm).pack(pady=3)

        supplementary_info = {
            "Category": self.info_note[0]["note_category"].upper(),
            "Date of addition": str(self.info_note[0]["created_at"])[:10],
            "Time of addition": str(self.info_note[0]["created_at"])[10:],
        }
        for title, info in supplementary_info.items():
            Label(
                supplementary_frame,
                text=title.upper(),
                width=20,
                bg=PALETTE["main"]["3color"],
                fg=PALETTE["text"]["2color"],
                font=("Arial", 12, "bold"),
            ).pack(pady=2)
            Label(
                supplementary_frame,
                text=info,
                width=20,
                bg=PALETTE["text"]["2color"],
                fg=PALETTE["main"]["3color"],
                font=("Arial", 12, "bold"),
            ).pack(pady=10)

    def _draw_update_button(self, note_id: int):
        """
        Draws the update button for saving changes to the note.

        Args:
            note_id (int): The ID of the note.
        """
        number_allowed_characters_name = NotesDatabaseAction.select_number_characters(
            "notes_info", "note_name")
        number_allowed_characters_desc = NotesDatabaseAction.select_number_characters(
            "notes_info", "note_description")

        update_comm = lambda: (
            self.open_note_information(note_id)
            if NoteDataSaver.updating_received_data(
                self.name_text_area,
                self.desc_text_area,
                self.info_note[0]["note_category"],
                self.nested_data,
                number_allowed_characters_name,
                number_allowed_characters_desc,
                note_id,
            )
            else None
        )

        self.update_button = Button(
            self.main_frame,
            text="Update",
            border=3, relief="flat",
            disabledforeground=PALETTE["text"]["3color"],
            disabledbackground=PALETTE["main"]["1color"],
            activebackground=PALETTE["secondary"]["1color"],
            activeforeground=PALETTE["text"]["2color"],
            state="disabled",
            command=update_comm)
        self.update_button.place(x=665, y=515)

    def _create_triangle_of_changes(self, previous_actions: Set[str]):
        """
        Creates the triangle of changes indicators for note name and description text areas.

        Args:
            previous_actions (Set[str]): A set containing the previous changes made to the note.
        """
        variation_triangle_name = Canvas(
            self.data_note_frame,
            width=15,
            height=15,
            bg=PALETTE["main"]["3color"],
            highlightthickness=0,
            relief="flat",
        )
        variation_triangle_desc = Canvas(
            self.data_note_frame,
            width=15,
            height=15,
            bg=PALETTE["main"]["3color"],
            highlightthickness=0,
            relief="flat",
        )

        start_x, start_y = 5, 15
        end_x, end_y = 15, 15
        corner_x, corner_y = 15, 5

        variation_triangle_name.create_polygon(
            start_x, start_y, end_x, end_y, corner_x, corner_y,
            fill=PALETTE["secondary"]["1color"],
        )
        variation_triangle_desc.create_polygon(
            start_x, start_y, end_x, end_y, corner_x, corner_y,
            fill=PALETTE["secondary"]["1color"],
        )

        self.name_text_area.bind(
            "<KeyRelease>",
            lambda e, area=self.name_text_area: self.check_changes_in_areas(
                area, variation_triangle_name, variation_triangle_desc, previous_actions
            ),
        )
        self.desc_text_area.bind(
            "<KeyRelease>",
            lambda e, area=self.desc_text_area: self.check_changes_in_areas(
                area, variation_triangle_name, variation_triangle_desc, previous_actions
            ),
        )

    def check_changes_in_areas(
            self,
            text_area: Text,
            variation_triangle_name: Canvas,
            variation_triangle_desc: Canvas,
            previous_actions: set,
    ):
        """
        Checks for changes in the text areas of the note's title or description
        and adds change triangles if there are changes

        Args:
            text_area (tkinter.Text): The text area widget to check for changes.
            variation_triangle_name (tkinter.Canvas): The canvas for the variation triangle
            of the note name.
            variation_triangle_desc (tkinter.Canvas): The canvas for the variation triangle
            of the note description.
            previous_actions (set): A set containing the previous changes made to the note.
        """
        column_of_change = (
            "note_description" if text_area == self.desc_text_area else "note_name"
        )
        current_content = text_area.get("1.0", "end-1c")
        original_content = self.info_note[0][column_of_change]
        if current_content != original_content:
            self.update_button.config(
                state="normal",
                bg=PALETTE["secondary"]["1color"],
                fg=PALETTE["text"]["1color"],
            )
            previous_actions.add(column_of_change)
        else:
            if column_of_change in previous_actions:
                previous_actions.remove(column_of_change)

            if len(previous_actions) == 0:
                self.update_button.config(state="disabled")

        triangles = {
            "note_name": variation_triangle_name,
            "note_description": variation_triangle_desc,
        }

        for key_t, triangle in triangles.items():
            if not triangle.winfo_ismapped() and key_t in previous_actions:
                triangle_place_coords = (605, 77) if key_t == "note_name" else (605, 527)
                triangle.place(x=triangle_place_coords[0], y=triangle_place_coords[1])
            elif triangle.winfo_ismapped() and key_t not in previous_actions:
                triangle.place_forget()
