from database.category_database_action import CategoryDatabaseAction
from lib_imports import PALETTE, Event, Frame, Listbox
from note_list_viewer import NoteListViewer
from operation_button_manager import OperationButtonManager


class SideCategoryList:
    """
    A class representing a side category list, which is responsible for
    creating a list of categories and displaying them in the interface.
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create and return a new instance of the SideCategoryList class,
        or return an existing instance if one already exists.
        """
        if cls.__instance is None:
            cls.__instance = super(SideCategoryList, cls).__new__(cls)
        return cls.__instance

    def __init__(self, main_window, operation_buttons_window, side_window):
        """
        Initializes the SideCategoryList class.

        Args:
            main_window (tkinter.Frame): The main application frame in the window.
            operation_buttons_window (tkinter.Frame): The frame for the operation buttons
                                              in the application window.
            side_window (tkinter.Frame): The frame for the side category list.
        """
        self.side_frame = side_window
        self.main_frame = main_window
        self.operation_buttons_frame = operation_buttons_window
        self.actions_of_operation_buttons = OperationButtonManager(
            self.main_frame, self.operation_buttons_frame
        )
        self.list_notes = NoteListViewer(
            self.main_frame,
            self.operation_buttons_frame,
            self.actions_of_operation_buttons,
        )
        self.side_listbox_categories = None
        self.active_item: int = 0

    def create_side_category_list(self):
        """
        Creates the side category list and displays the categories.
        """
        if hasattr(self, "frame_categories"):
            self.frame_categories.destroy()

        frame_categories = Frame(self.side_frame)
        frame_categories.place(x=8, y=30)

        self.side_listbox_categories = Listbox(
            frame_categories,
            width=15,
            border=0,
            fg=PALETTE["text"]["1color"],
            font=("Arial", 20),
            relief="flat",
            activestyle="none",
            bg=PALETTE["main"]["2color"],
            height=15,
            selectbackground=PALETTE["main"]["2color"],
        )

        # Getting all categories into a list from the database
        self.add_categories()
        self.list_notes.create_note_display_interface()

        # Bind event handlers to the list
        for event in ("<<ListboxSelect>>", "<ButtonRelease-1>"):
            self.side_listbox_categories.bind(event, self._category_selector_control)

        # Set the default active item
        self.side_listbox_categories.selection_set(0)
        self._update_color_side_listbox()
        self.side_listbox_categories.pack(side="left", fill="both", expand=True)

    def add_categories(self):
        """
        Adds the categories to the side listbox.
        """
        all_database_categories = CategoryDatabaseAction.all_categories_list(
            "note_category")
        all_database_categories.insert(0, "All notes")

        # Add the resulting categories to the area
        for category in all_database_categories:
            self.side_listbox_categories.insert("end", category)

    def _category_selector_control(self, event: Event):
        """
        Controls the category selection in the side listbox.

        Args:
            event(tkinter.Event): The event object.
        """
        widget = event.widget
        selection = widget.curselection()
        if selection:
            item_index = selection[0]
            if item_index != self.active_item:
                self.side_listbox_categories.selection_clear(self.active_item)
                self.active_item = item_index
                self.side_listbox_categories.selection_set(self.active_item)
                self._update_color_side_listbox()
                side_listbox_active_category = widget.get(self.active_item)

                for widget in self.main_frame.winfo_children():
                    widget.destroy()

                self.actions_of_operation_buttons.destroy_dynamic_buttons()

                self.list_notes.create_note_display_interface(
                    note_category=side_listbox_active_category)

    def _update_color_side_listbox(self):
        """
        Color management of the active category.
        """
        # Updating the color of the active item
        for item in range(self.side_listbox_categories.size()):
            if item == self.active_item:
                self.side_listbox_categories.itemconfig(
                    item, selectforeground=PALETTE["text"]["1color"])
            else:
                self.side_listbox_categories.itemconfig(
                    item, fg=PALETTE["text"]["3color"])
