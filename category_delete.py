from lib_imports import messagebox
from database.category_database_action import CategoryDatabaseAction
from side_category_list import SideCategoryList
from database.notes_database_action import NotesDatabaseAction


class CategoryDelete:
    """
    Represents a category deletion manager.
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create and return a new instance of the CategoryDelete class,
        or return an existing instance if one already exists.
        """
        if cls.__instance is None:
            cls.__instance = super(CategoryDelete, cls).__new__(cls)
        return cls.__instance

    def __init__(self, main_window, operation_buttons_window, side_window):
        """
        Initializes the CategoryDelete class.

        Args:
            main_window (tkinter.Tk): The main application window.
            operation_buttons_window (tkinter.Frame): The frame for the operation buttons.
            side_window (tkinter.Frame): The side window.
        """
        self.side_frame = side_window
        self.main_frame = main_window
        self.operation_buttons_frame = operation_buttons_window
        self.side_listbox_categories = SideCategoryList(
            self.main_frame, self.operation_buttons_frame, self.side_frame
        )

    def create_message_delete_category(self):
        """
        Creates a message box to confirm category deletion and performs the deletion if confirmed.
        """
        if self.side_listbox_categories.side_listbox_active_category != "All notes":
            answer = messagebox.askokcancel(
                "Delete Category",
                "Are you sure you want to delete the category:\n"
                f"{self.side_listbox_categories.side_listbox_active_category}\n"
                f"If this category has notes "
                "they will also be deleted?",
            )
            if answer:
                CategoryDatabaseAction.delete_category(
                    "note_category",
                    self.side_listbox_categories.side_listbox_active_category,
                )
                NotesDatabaseAction.delete_all_note_in_category(
                    "notes_info",
                    self.side_listbox_categories.side_listbox_active_category,
                )
            self.side_listbox_categories.create_side_category_list()
        else:
            messagebox.showinfo("Message", "Select a category to delete")
