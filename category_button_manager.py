from lib_imports import *
from category_creator import CategoryCreator


class CategoryButtonManager:
    def __init__(self, side_window, main_window, operation_buttons_window):
        self.side_frame = side_window
        self.main_frame = main_window
        self.operation_buttons_frame = operation_buttons_window

        self.category_button_add = CategoryCreator(self.main_frame,
                                                   self.operation_buttons_frame,
                                                   self.side_frame)

    def start(self):
        add_button = Button(self.side_frame, text="Add category",
                            bg=PALETTE["main"]["1color"],
                            font=("Arial", 14),
                            fg=PALETTE["text"]["2color"],
                            activebackground=PALETTE["main"]["3color"],
                            activeforeground=PALETTE["text"]["1color"],
                            width=175, height=18,
                            border=4, relief="flat",
                            command=self.category_button_add.create_interface_add_category_win
                            )
        add_button.place(x=5, y=400)

        category_add = lambda: self.create_interface_setup_category_tab()
        setup_button = Button(self.side_frame, text="Setup categories",
                              bg=PALETTE["main"]["1color"],
                              font=("Arial", 14),
                              fg=PALETTE["text"]["2color"],
                              activebackground=PALETTE["main"]["3color"],
                              activeforeground=PALETTE["text"]["1color"],
                              width=175, height=18,
                              border=4, relief="flat",
                              )
        setup_button.place(x=5, y=435)

    def create_interface_add_category_tab(self):
        pass

    def create_interface_setup_category_tab(self):
        pass
