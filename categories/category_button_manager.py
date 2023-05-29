from categories.category_creator import CategoryCreator
from categories.category_delete import CategoryDelete
from categories.category_edit import CategoryEdit
from lib_imports import PALETTE, Label, Canvas, Button, webbrowser


class CategoryButtonManager:
    """
    Manages the category buttons in the application.
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create and return a new instance of the CategoryButtonManager class,
        or return an existing instance if one already exists.
        """
        if cls.__instance is None:
            cls.__instance = super(CategoryButtonManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self, side_window, main_window, operation_buttons_window):
        """
        Initializes the CategoryButtonManager class.

        Args:
            side_window (tkinter.Frame): The side window frame.
            main_window (tkinter.Frame): The main application frame.
            operation_buttons_window (tkinter.Frame): The operation buttons frame.
        """
        self.side_frame = side_window
        self.main_frame = main_window
        self.operation_buttons_frame = operation_buttons_window

        self.category_button_add = CategoryCreator(
            self.main_frame, self.operation_buttons_frame, self.side_frame
        )
        self.cat_setup = CategoryEdit(
            self.main_frame, self.operation_buttons_frame, self.side_frame
        )
        self.cat_delete = CategoryDelete(
            self.main_frame, self.operation_buttons_frame, self.side_frame
        )

    def create_category_buttons(self):
        """
        Creates the category buttons and information about the program.
        """
        self._draw_line_under_list_categories()

        self._draw_button_add_category()

        self._draw_button_edit_category()

        self._draw_button_delete_category()

        self._draw_information_about_program()

    def _draw_line_under_list_categories(self):
        """
        Draws a line under the list of categories.
        """
        line_canvas = Canvas(
            self.side_frame,
            width=200,
            height=1,
            highlightthickness=1,
            highlightbackground=PALETTE["main"]["2color"],
            background=PALETTE["secondary"]["1color"],
        )
        line_canvas.place(x=-4, y=445)
        line_canvas.create_line(50, 100, 350, 100)

    def _draw_button_add_category(self):
        """
        Draws the 'Add category' button.
        """
        add_button = Button(
            self.side_frame,
            text="Add category",
            bg=PALETTE["main"]["1color"],
            font=("Arial", 14),
            fg=PALETTE["text"]["2color"],
            activebackground=PALETTE["main"]["3color"],
            activeforeground=PALETTE["text"]["1color"],
            width=175,
            height=18,
            border=4,
            relief="flat",
            command=self.category_button_add.create_interface_add_category_win,
        )
        add_button.place(x=6, y=465)

    def _draw_button_edit_category(self):
        """
        Draws the 'Edit category' button.
        """
        category_edit = lambda: self.cat_setup.create_interface_edit_category_win()
        edit_button = Button(
            self.side_frame,
            text="Edit category",
            bg=PALETTE["main"]["1color"],
            font=("Arial", 14),
            fg=PALETTE["text"]["2color"],
            activebackground=PALETTE["main"]["3color"],
            activeforeground=PALETTE["text"]["1color"],
            width=175,
            height=18,
            border=4,
            relief="flat",
            command=category_edit,
        )
        edit_button.place(x=6, y=500)

    def _draw_button_delete_category(self):
        """
        Draws the 'Delete category' button.
        """
        category_delete = lambda: self.cat_delete.create_message_delete_category()
        delete_button = Button(
            self.side_frame,
            text="Delete category",
            bg=PALETTE["main"]["1color"],
            font=("Arial", 14),
            fg=PALETTE["text"]["2color"],
            activebackground=PALETTE["main"]["3color"],
            activeforeground=PALETTE["text"]["1color"],
            width=175,
            height=18,
            border=4,
            relief="flat",
            command=category_delete,
        )
        delete_button.place(x=6, y=535)

    def _draw_information_about_program(self):
        """
        Draws the GitHub link.
        """
        before_link_text = Label(
            text="Our git: ",
            bg=PALETTE["main"]["2color"],
            font=("Arial", 14),
            fg=PALETTE["text"]["1color"],
        )
        before_link_text.place(x=19, y=572)
        my_link_in_browser = Label(
            text="app-Quick-Notes",
            bg=PALETTE["main"]["2color"],
            font=("Arial", 14),
            fg=PALETTE["secondary"]["1color"],
            activeforeground=PALETTE["text"]["2color"],
        )
        my_link_in_browser.place(x=71, y=572)
        my_link_in_browser.bind("<Button-1>", lambda e: self.open_git_link())

    @staticmethod
    def open_git_link():
        """
        Opens the GitHub link in a web browser.
        """
        url = "https://github.com/nikitach507/app-Quick-Notes"
        webbrowser.open_new(url)
