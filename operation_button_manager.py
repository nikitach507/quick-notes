from lib_imports import PALETTE, Button
from note_creator import NoteCreator
from note_display_window import NoteDisplayWindow
from note_list_viewer import NoteListViewer


class OperationButtonManager:
    """
    A class representing the manager of operation buttons.
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create and return a new instance of the OperationButtonManager class,
        or return an existing instance if one already exists.
        """
        if cls.__instance is None:
            cls.__instance = super(OperationButtonManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self, main_window, operation_buttons_window, cat_side_obj):
        """
        Initializes the OperationButtonManager class.

        Args:
            main_window (tkinter.Frame): The main application frame in the window.
            operation_buttons_window (tkinter.Frame): The frame for the operation buttons
                                              in the application window.
        """
        self.operation_buttons_frame = operation_buttons_window
        self.main_frame = main_window
        self.operation_button_add = NoteCreator(self.main_frame)
        self.notes_list = NoteListViewer(
            self.main_frame, self.operation_buttons_frame, self
        )
        self.cat_side_obj = cat_side_obj
        self.pop_up_buttons = {}
        self.note_operation_buttons = None
        self.x_note_buttons = None

    def create_operation_buttons(self):
        """
        Creates and draws operating buttons on the frame for the operation buttons.
        """
        self.note_operation_buttons = {"create new note": self.switch_add_note}
        self.x_note_buttons = 0
        for caption, button_function in self.note_operation_buttons.items():
            self.draw_operating_button(
                button_symbol=caption, button_action=button_function)

    def switch_add_note(self):
        """
        Deletes all widgets from main_frame and pops up a window for adding a new note.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.destroy_dynamic_buttons()

        cat = self.cat_side_obj.side_listbox_active_category

        self.cat_side_obj.create_side_category_list(cat)

        self.operation_button_add.create_interface_add_note_tab(cat)

    def draw_operating_button(self, button_symbol: str, button_action: callable):
        """
        Draws an operating button with a given caption
        and an associated action on the operation_buttons_frame.
        Stores the button in pop_up_buttons if it is not a "create new note" button.

        Args:
            button_symbol (str): the text on the button.
            button_action (callable): a function or method to be called
                                      when the button is clicked.
        """
        operating_button_command = lambda: button_action()
        created_oper_button = Button(
            self.operation_buttons_frame,
            text=f"{button_symbol}",
            bg=PALETTE["main"]["1color"],
            font=("Georgia", 14),
            fg=PALETTE["text"]["2color"],
            activebackground=PALETTE["main"]["1color"],
            activeforeground=PALETTE["text"]["1color"],
            width=120, height=18,
            border=4, relief="flat",
            command=operating_button_command,
        )
        if button_symbol != "create new note":
            self.pop_up_buttons[button_symbol] = created_oper_button
        created_oper_button.place(x=self.x_note_buttons, y=-2)
        self.x_note_buttons += 130

    def add_dynamic_buttons(self, note_id: int, note_category: str):
        """
        Destroys all dynamic buttons and creates two new buttons: one to delete a note
        and another to display a note window.

        Args:
            note_id (int): The id of the note to which the buttons will be added.
            note_category (str): The note category, which will be deleted.
        """
        self.destroy_dynamic_buttons()

        delete_note_lambda = lambda: (
            self.notes_list.delete_note_button(note_id, note_category),
            self.destroy_dynamic_buttons())

        note_window = NoteDisplayWindow()
        window_note_lambda = lambda: note_window.create_new_window(note_id)

        self.x_note_buttons = 130
        self.draw_operating_button(
            button_symbol="delete the note", button_action=delete_note_lambda)
        self.draw_operating_button(
            button_symbol="note window", button_action=window_note_lambda)

    def destroy_dynamic_buttons(self):
        """
        Destroys all pop-up buttons from the operation_buttons_frame.
        """
        if len(self.pop_up_buttons) == 2:
            for pop_up_button in self.pop_up_buttons.values():
                pop_up_button.destroy()
