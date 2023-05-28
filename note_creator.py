from database.category_database_action import CategoryDatabaseAction
from database.notes_database_action import NotesDatabaseAction
from lib_imports import (PALETTE, Button, Event, Frame, Label, Listbox,
                         Scrollbar, Text)
from note_data_saver import NoteDataSaver
from note_information import NoteInformation


class NoteCreator:
    """
    Class that works with the addition of a new note
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create and return a new instance of the NoteCreator class,
        or return an existing instance if one already exists.
        """
        if cls.__instance is None:
            cls.__instance = super(NoteCreator, cls).__new__(cls)
        return cls.__instance

    def __init__(self, main_window, operation_window, side_object):
        """
        Initializes the NoteCreator class.

        Args:
            main_window (tkinter.Frame): The main application frame in the window.
        """
        self.main_frame = main_window
        self.operation_buttons_frame = operation_window
        self.side_object = side_object
        self.note_information_obj = NoteInformation(
            self.main_frame, self.operation_buttons_frame, self.side_object
        )
        self.selected_category = ""
        self.active_item = 0
        self.name_text_form = None
        self.desc_text_form = None
        self.name_char_count_error = None
        self.desc_char_count_error = None

    def create_interface_add_note_tab(self, current_category):
        """
        Create a window interface for adding notes
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self._draw_window_title()
        self._draw_area_name_note()
        self._draw_area_description_note()
        self._draw_area_category_note(current_category)

        number_allowed_characters_name = NotesDatabaseAction.select_number_characters(
            "notes_info", "note_name")
        number_allowed_characters_desc = NotesDatabaseAction.select_number_characters(
            "notes_info", "note_description")

        for form in (self.name_text_form, self.desc_text_form):
            form.bind(
                "<KeyRelease>",
                lambda e: self.check_input_data_length(
                    number_allowed_characters_name, number_allowed_characters_desc))

        nested_data = {"note_name": self.name_text_form, "note_description": self.desc_text_form}
        self.selected_category = current_category
        self._draw_area_save_note(
            nested_data, number_allowed_characters_name, number_allowed_characters_desc)

    def _draw_window_title(self):
        """
        Draw the title label for the window.
        """
        header_label = Label(
            self.main_frame,
            text="CREATE A NOTE",
            bg=PALETTE["main"]["3color"],
            fg=PALETTE["text"]["1color"],
            font=("Arial", 15, "bold"),
            anchor="w",
        )
        header_label.pack(padx=10, pady=10, anchor="nw")

    def _draw_area_name_note(self):
        """
        Draw the text area for the note name.
        """
        self.name_text_form = Text(
            self.main_frame,
            height=1, width=39,
            bg=PALETTE["secondary"]["2color"],
            wrap="none", undo=True,
            border=3, relief="flat",
            selectborderwidth=0,
            highlightthickness=0,
            font=("Arial", 24, "bold"),
            fg=PALETTE["main"]["3color"],
            insertbackground=PALETTE["main"]["2color"],
        )
        self.name_text_form.pack(padx=10, pady=3, anchor="nw")

    def _draw_area_description_note(self):
        """
        Draw the text area for the note description.
        """
        self.desc_text_form = Text(
            self.main_frame,
            height=20, width=60,
            bg=PALETTE["secondary"]["2color"],
            wrap="word", undo=True,
            border=2, relief="flat",
            selectborderwidth=0,
            highlightthickness=0,
            font=("Arial", 16),
            fg=PALETTE["main"]["3color"],
            tabs=15, tabstyle="tabular",
            spacing1=5, padx=5,
            insertbackground=PALETTE["main"]["2color"],
        )
        self.desc_text_form.pack(padx=10, pady=0, anchor="nw")

    def _draw_area_save_note(
            self,
            nested_data: dict,
            number_allowed_characters_name: int,
            number_allowed_characters_desc: int):
        """
        Draws the area for saving a note with a button to add data to the database.

        Args:
            nested_data (dict): Nested data containing the name and description of the note.
            number_allowed_characters_name (int): The maximum number of characters allowed
            for the note name.
            number_allowed_characters_desc (int): The maximum number of characters allowed
            for the note description.
        """

        saving_comm = lambda: self._saving_data(nested_data,
                                                number_allowed_characters_name,
                                                number_allowed_characters_desc)
        # Create a button to add data to the database
        save_button = Button(
            self.main_frame,
            text="Save",
            bg=PALETTE["secondary"]["1color"],
            fg=PALETTE["text"]["1color"],
            activebackground=PALETTE["secondary"]["1color"],
            border=3, relief="flat",
            activeforeground=PALETTE["text"]["2color"],
            command=saving_comm,
        )
        save_button.place(x=670, y=515)

    def _saving_data(self, nested_data: dict,
                     number_allowed_characters_name: int,
                     number_allowed_characters_desc: int):
        NoteDataSaver.saving_received_data(
            save_name_form=self.name_text_form,
            save_desc_form=self.desc_text_form,
            current_category=self.selected_category,
            nested_data=nested_data,
            allowed_characters_name=number_allowed_characters_name,
            allowed_characters_desc=number_allowed_characters_desc,
            note_information_object=self.note_information_obj,
        )
        self.selected_category = ""
        #

    def _draw_area_category_note(self, current_category):
        """
        Draws the area for selecting a category for the note.
        """
        category_name_label = Label(
            self.main_frame,
            text="CATEGORY(*):",
            bg=PALETTE["main"]["3color"],
            fg=PALETTE["secondary"]["2color"],
            font=("Arial", 13, "bold"),
        )
        category_name_label.place(x=580, y=10)
        if current_category == "All notes":
            # Creating a frame for selecting categories
            select_category_frame = Frame(
                self.main_frame,
                bg=PALETTE["main"]["3color"],
                highlightbackground=PALETTE["main"]["1color"],
                highlightcolor=PALETTE["main"]["1color"],
                highlightthickness=2,
                padx=2, pady=2,
            )
            select_category_frame.place(x=580, y=45)

            category_listbox = Listbox(
                select_category_frame,
                width=19, height=7,
                font=("Arial", 15),
                bg=PALETTE["main"]["3color"],
                border=0, relief="flat",
                activestyle="none",
                fg=PALETTE["text"]["2color"],
                selectbackground=PALETTE["main"]["1color"],
            )
            category_listbox_scrollbar = Scrollbar(
                select_category_frame,
                command=category_listbox.yview,
                troughcolor=PALETTE["main"]["3color"],
            )
            category_listbox.configure(yscrollcommand=category_listbox_scrollbar.set)

            self._category_list_management(category_listbox, category_listbox_scrollbar)
        else:
            Label(
                self.main_frame,
                text=current_category.upper(),
                width=20,
                bg=PALETTE["text"]["2color"],
                fg=PALETTE["main"]["3color"],
                font=("Arial", 12, "bold"),
                anchor="w"
            ).place(x=583, y=46)
            # self.selected_category = current_category

    def _category_list_management(
            self, category_listbox: Listbox, category_listbox_scrollbar: Scrollbar):
        """
        Manages the category listbox by populating it with categories and setting event handlers.

        Args:
            category_listbox (tkinter.Listbox): The listbox widget for displaying categories.
            category_listbox_scrollbar (tkinter.Scrollbar): The scrollbar widget associated
            with the category listbox.
        """
        # Getting all categories into a list from the database
        all_database_categories = CategoryDatabaseAction.all_categories_list(
            "note_category")
        all_database_categories.insert(0, "")

        # Add the resulting categories to the area
        for category in all_database_categories:
            category_listbox.insert("end", category)

        # Bind event handlers to the list
        for event in ("<<ListboxSelect>>", "<ButtonRelease-1>"):
            category_listbox.bind(
                event,
                lambda e: self._category_selector_control(e, category_listbox))

        # Set the default active item
        category_listbox.selection_set(0)
        self.active_item = 0
        # self._update_color_category_listbox(category_listbox)

        category_listbox.pack(side="left", fill="both", expand=True)
        category_listbox_scrollbar.pack(side="left", fill="y")

    def _category_selector_control(self, event: Event, category_listbox: Listbox):
        """
        Event handler for selecting a category from the listbox.

        Args:
            event (tkinter.Event): The event object triggered by selecting a category.
            category_listbox (Listbox): The listbox widget for displaying categories.
        """
        # List item selection event handler
        widget = event.widget
        selection = widget.curselection()
        if selection:
            item_index = selection[0]
            if item_index != self.active_item:
                category_listbox.selection_clear(self.active_item)
                self.active_item = item_index
                self._update_color_category_listbox(category_listbox)
                self.selected_category = widget.get(self.active_item)

    def _update_color_category_listbox(self, category_listbox: Listbox):
        """
        Updates the color of the active item in the category listbox.

        Args:
            category_listbox (Listbox): The listbox widget for displaying categories.
        """
        # Updating the color of the active item
        for item in range(category_listbox.size()):
            if item == self.active_item:
                category_listbox.itemconfig(item,
                                            fg=PALETTE["text"]["1color"],
                                            bg=PALETTE["main"]["1color"],
                                            selectforeground=PALETTE["text"]["1color"])
            else:
                category_listbox.itemconfig(item,
                                            fg=PALETTE["text"]["2color"],
                                            bg=PALETTE["main"]["3color"])

    def check_input_data_length(
            self, allowed_characters_name: int, allowed_characters_desc: int):
        """
        Checks the length of the input data (note name and description)
        and displays an error message if it exceeds the allowed length.

        Args:
            allowed_characters_name (int): The maximum number of characters allowed
            for the note name.
            allowed_characters_desc (int): The maximum number of characters allowed
            for the note description.
        """
        current_count_name = len(self.name_text_form.get("1.0", "end-1c"))
        current_count_desc = len(self.desc_text_form.get("1.0", "end-1c"))

        self.name_char_count_error = self.check_field_length(
            allowed_characters_name,
            current_count_name,
            self.name_char_count_error,
            "header")

        self.desc_char_count_error = self.check_field_length(
            allowed_characters_desc,
            current_count_desc,
            self.desc_char_count_error,
            "description")

    def check_field_length(
            self, allowed_characters: int, current_count: int, error_label, field_name: str):
        """
        Checks the length of a field and displays an error message if it exceeds the allowed length.

        Args:
            allowed_characters (int): The maximum number of characters allowed for the field.
            current_count (int): The current number of characters in the field.
            error_label: The label widget for displaying the error message.
            field_name (str): The name of the field.

        Returns:
            error_label: The label widget for displaying the error message.
        """
        error_message = (
            (
                f"Maximum number of characters in the {field_name}: {allowed_characters}.\n"
                f"Current count: {current_count}"
            ) if current_count > allowed_characters else None
        )

        if error_label is not None:
            error_label.destroy()

        if error_message is not None:
            error_label = Label(
                self.main_frame,
                text=error_message,
                bg=PALETTE["main"]["3color"],
                wraplength=190,
                justify="left",
                fg=PALETTE["secondary"]["4color"])

            if field_name == "header":
                error_label.place(x=580, y=200)
            else:
                error_label.place(x=580, y=280)

        return error_label
