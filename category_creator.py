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
        new_window = Toplevel()
        new_window.title("ADD A NEW CATEGORY")
        new_window.resizable(False, False)
        new_window.grab_set()
        new_window.attributes("-topmost", True)

        # Получить ширину и высоту монитора
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()

        # Получить ширину и высоту окна
        window_width = 400
        window_height = 150

        # Рассчитать координаты окна для его расположения в центре монитора
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Установить координаты окна
        new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        new_window.configure(bg=PALETTE["main"]["1color"])

        self.draw_input_category(new_window)
        self.draw_button_add(new_window)

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
        saving_comm = lambda: (CategoryDatabaseAction().add_category("note_category", self.input_cat.get()),
                               self.close_window_after_adding(window))

        button = Button(window, text="Add", bg=PALETTE["secondary"]["1color"],
                        fg=PALETTE["text"]["1color"],
                        activebackground=PALETTE["main"]["3color"],
                        activeforeground=PALETTE["text"]["1color"],
                        width=130, height=20,
                        command=saving_comm,
                        )
        button.place(x=136, y=80)

    def close_window_after_adding(self, window):
        window.destroy()
        self.side_listbox_categories.create_side_category_list()



