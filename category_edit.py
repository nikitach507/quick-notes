from database.category_database_action import CategoryDatabaseAction
from database.notes_database_action import NotesDatabaseAction
from lib_imports import PALETTE, Toplevel, messagebox, Entry, Button, Label
from side_category_list import SideCategoryList


class CategoryEdit:
    """
    Represents a category editing manager.
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create and return a new instance of the CategoryEdit class,
        or return an existing instance if one already exists.
        """
        if cls.__instance is None:
            cls.__instance = super(CategoryEdit, cls).__new__(cls)
        return cls.__instance

    def __init__(self, main_window, operation_buttons_window, side_window):
        """
        Initializes the CategoryEdit class.

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
        self.error_message = None
        self.input_category = None

    def create_interface_edit_category_win(self):
        """
        Creates the interface for editing a category.
        """
        if self.side_listbox_categories.side_listbox_active_category != "All notes":
            edit_window = Toplevel()
            edit_window.title("EDIT THE CATEGORY NAME")
            edit_window.resizable(False, False)
            edit_window.grab_set()
            edit_window.attributes("-topmost", True)

            screen_width = edit_window.winfo_screenwidth()
            screen_height = edit_window.winfo_screenheight()
            window_width = 400
            window_height = 150
            window_x = (screen_width - window_width) // 2
            window_y = (screen_height - window_height) // 2

            edit_window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
            edit_window.configure(bg=PALETTE["main"]["1color"])

            self._draw_input_category(edit_window)
            self._draw_button_edit(edit_window)
        else:
            messagebox.showinfo("Message", "Select a category to change")

    def _draw_input_category(self, window: Toplevel):
        """
        Draws the input field for entering the category name.

        Args:
            window (tkinter.Toplevel): The edit window.
        """
        self.input_category = Entry(
            window,
            bg=PALETTE["main"]["3color"],
            width=40,
            cursor="ibeam",
            font=("Arial", 16),
            bd=3,
            relief="flat",
            highlightthickness=2,
            highlightcolor=PALETTE["main"]["3color"],
            highlightbackground=PALETTE["main"]["3color"],
        )

        self.input_category.insert(
            0, self.side_listbox_categories.side_listbox_active_category
        )
        self.input_category.pack(pady=40, anchor="center")

    def _draw_button_edit(self, window: Toplevel):
        """
        Draws the edit button.

        Args:
            window (tkinter.Toplevel): The edit window.
        """
        editing_comm = lambda: self._action_after_press_edit(
            window, self.input_category.get()
        )

        button = Button(
            window,
            text="Edit",
            bg=PALETTE["secondary"]["1color"],
            fg=PALETTE["text"]["1color"],
            activebackground=PALETTE["main"]["3color"],
            activeforeground=PALETTE["text"]["1color"],
            width=130,
            height=20,
            command=editing_comm,
        )
        button.place(x=136, y=80)

    def _action_after_press_edit(self, window: Toplevel, current_input: str):
        """
        Performs the edit action after pressing the edit button.

        Args:
            window (tkinter.Toplevel): The edit window.
            current_input (str): The new category name entered by the user.
        """
        if self.check_input_data(window, current_input):
            CategoryDatabaseAction().edit_category(
                "note_category",
                self.side_listbox_categories.side_listbox_active_category,
                current_input,
            )
            NotesDatabaseAction.edit_category_in_note(
                "notes_info",
                self.side_listbox_categories.side_listbox_active_category,
                current_input,
            )
            self.close_window_after_adding(window, current_input)

    def check_input_data(self, window: Toplevel, current_input: str):
        """
        Checks the input data for the category name.

        Args:
            window (tkinter.Toplevel): The edit window.
            current_input (str): The new category name entered by the user.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        allowed_characters = CategoryDatabaseAction.select_number_characters(
            "note_category", "name_cat"
        )
        all_database_categories = CategoryDatabaseAction.all_categories_list(
            "note_category"
        )

        if len(current_input) > allowed_characters or len(current_input) < 1:
            if self.error_message:
                self.error_message.destroy()
            self.error_message = Label(
                window,
                text=f"Category names must be between 1 and {allowed_characters} characters.\n"
                     f"Current count: {len(current_input)}",
                justify="left",
                bg=PALETTE["main"]["1color"],
                fg=PALETTE["secondary"]["4color"],
            )
            self.error_message.place(x=12, y=3)
            return False
        if current_input in all_database_categories:
            if self.error_message:
                self.error_message.destroy()
            self.error_message = Label(
                window,
                text=f"The name of the category {current_input} already exists",
                justify="left",
                bg=PALETTE["main"]["1color"],
                fg=PALETTE["secondary"]["4color"],
            )
            self.error_message.place(x=12, y=10)
            return False
        return True

    def close_window_after_adding(self, window: Toplevel, current_input: str):
        """
        Closes the window after successfully adding a category.

        Args:
            window (tkinter.Toplevel): The edit window.
            current_input (str): The new category name entered by the user.
        """
        window.destroy()
        self.side_listbox_categories.create_side_category_list(
            note_category=current_input
        )
