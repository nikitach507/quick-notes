from lib_imports import PALETTE, Frame, Tk
from operation_button_manager import OperationButtonManager
from side_category_list import SideCategoryList
from category_button_manager import CategoryButtonManager


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
        self.actions_of_operation_buttons = OperationButtonManager(
            self.main_window, self.upper_window
        )
        self.side_listbox_categories = SideCategoryList(
            self.main_window, self.upper_window, self.side_window
        )

        self.actions_of_category_buttons = CategoryButtonManager(
            self.side_window, self.main_window, self.upper_window
        )

    def create_app_interface(self):
        """
        Creates the application interface by creating buttons to control notes
        and a side list of categories.
        """
        # Creating buttons to control notes
        self.actions_of_operation_buttons.create_operation_buttons()

        # Creating a side list of categories
        self.side_listbox_categories.create_side_category_list()

        self.actions_of_category_buttons.start()


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

    app.create_app_interface()

    win.mainloop()
