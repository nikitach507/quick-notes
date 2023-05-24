from lib_imports import *
from database.category_database_action import CategoryDatabaseAction
from side_category_list import SideCategoryList


class CategoryCreator:
    def __init__(self, main_window, operation_buttons_window, side_window):
        self.side_frame = side_window
        self.main_frame = main_window
        self.operation_buttons_frame = operation_buttons_window
        self.side_listbox_categories = SideCategoryList(
            self.main_frame, self.operation_buttons_frame, self.side_frame
        )
        self.input_cat = None

    def create_interface_add_category_win(self):
        window_add_category = Toplevel()
        window_add_category.title("ADD A NEW CATEGORY")
        window_add_category.resizable(False, False)
        window_add_category.grab_set()
        window_add_category.attributes("-topmost", True)

        screen_width = window_add_category.winfo_screenwidth()
        screen_height = window_add_category.winfo_screenheight()

        window_width = 400
        window_height = 150

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        window_add_category.geometry(f"{window_width}x{window_height}+{x}+{y}")
        window_add_category.configure(bg=PALETTE["main"]["1color"])

        self.draw_input_category(window_add_category)
        self.draw_button_add(window_add_category)

    def draw_input_category(self, window):
        self.input_cat = Entry(window, bg=PALETTE["main"]["3color"], width=40,
                               cursor="ibeam",
                               font=("Arial", 16),
                               bd=3, relief="flat",
                               highlightthickness=2,
                               highlightcolor=PALETTE["main"]["3color"],
                               highlightbackground=PALETTE["main"]["3color"],
                               )
        self.input_cat.pack(pady=40, anchor="center")

    def draw_button_add(self, window):
        saving_comm = lambda: self._action_after_press_add(window, self.input_cat.get())

        button = Button(window, text="Add", bg=PALETTE["secondary"]["1color"],
                        fg=PALETTE["text"]["1color"],
                        activebackground=PALETTE["main"]["3color"],
                        activeforeground=PALETTE["text"]["1color"],
                        width=130, height=20,
                        command=saving_comm,
                        )
        button.place(x=136, y=80)

    def _action_after_press_add(self, window, current_input):
        CategoryDatabaseAction().add_category("note_category", current_input)
        self.close_window_after_adding(window, current_input)

    def close_window_after_adding(self, window, current_input):
        window.destroy()
        self.side_listbox_categories.create_side_category_list(note_category=current_input)



