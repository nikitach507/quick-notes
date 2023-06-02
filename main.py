from lib_imports import PALETTE, Frame, Tk, Label
from notes.operation_button_manager import OperationButtonManager
from categories.side_category_list import SideCategoryList
from categories.category_button_manager import CategoryButtonManager

from user_authentication import AuthenticationUser
from PIL import ImageTk, Image


class QuickNotesApp:
    """
    A class representing the QuickNotesApp application.
    """

    def __init__(self, upper_area, side_area, main_area):
        """
        Initializes the QuickNotesApp class.

        Args:
            upper_area (tkinter.Frame): The upper window frame.
            side_area (tkinter.Frame): The side window frame.
            main_area (tkinter.Frame): The main window frame.
        """
        self.upper_window = upper_area
        self.side_window = side_area
        self.main_window = main_area
        self.auth_interface = AuthenticationUser(
            self.side_window, self.main_window, self.upper_window
        )

    def user_auth(self, after_reg=None):
        self.auth_interface.user_auth(obj_main_app=self, after_reg=after_reg)

    def create_app_interface(self, user_id):
        """
        Creates the application interface by creating buttons to control notes
        and a side list of categories.
        """
        actions_of_category_buttons = CategoryButtonManager(
            self.side_window, self.main_window, self.upper_window, user_id
        )
        actions_of_operation_buttons = OperationButtonManager(
            self.main_window, self.upper_window, actions_of_category_buttons, user_id
        )
        side_listbox_categories = SideCategoryList(
            self.main_window, self.upper_window, self.side_window, user_id
        )
        # Creating buttons to control notes
        actions_of_operation_buttons.create_operation_buttons()

        # Creating a side list of categories
        side_listbox_categories.create_side_category_list()

        # Creating buttons for category management
        actions_of_category_buttons.create_category_buttons()


if __name__ == "__main__":
    win = Tk()
    win_width, win_height = 1000, 600
    win.title("Quick notes")
    win.geometry(f"{win_width}x{win_height}+200+150")
    win.resizable(False, False)

    side_frame = Frame(
        win,
        bg=PALETTE["main"]["2color"],
        border=3,
        relief="flat",
        width=200,
        highlightbackground=PALETTE["main"]["1color"],
    )
    side_frame.place(x=0, y=0, relheight=1)
    upper_frame = Frame(win, bg=PALETTE["main"]["1color"], height=30, border=4)
    upper_frame.place(x=200, y=0, relwidth=1)
    main_frame = Frame(win, bg=PALETTE["main"]["3color"], border=4)
    main_frame.place(x=200, y=30, relwidth=1, relheight=1)

    app = QuickNotesApp(upper_frame, side_frame, main_frame)

    image_tk = ImageTk.PhotoImage(Image.open("notes-logo.png").resize((200, 200)))
    image_tk_t = ImageTk.PhotoImage(Image.open("notes_logo_tr.png").resize((200, 200)))

    # Создание виджета Label и вставка изображения
    label = Label(side_frame, image=image_tk, border=0, relief="flat")
    label.place(x=-5, y=50)

    win.iconphoto(True, image_tk_t)

    app.user_auth()
    win.mainloop()
