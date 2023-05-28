from lib_imports import *
from category_creator import CategoryCreator
from category_edit import CategoryEdit
from category_delete import CategoryDelete


class CategoryButtonManager:
    def __init__(self, side_window, main_window, operation_buttons_window):
        self.side_frame = side_window
        self.main_frame = main_window
        self.operation_buttons_frame = operation_buttons_window

        self.category_button_add = CategoryCreator(self.main_frame,
                                                   self.operation_buttons_frame,
                                                   self.side_frame)
        self.cat_setup = CategoryEdit(self.main_frame,
                                      self.operation_buttons_frame,
                                      self.side_frame)
        self.cat_delete = CategoryDelete(self.main_frame,
                                         self.operation_buttons_frame,
                                         self.side_frame)

    def create_category_buttons(self):
        line_canvas = Canvas(self.side_frame, width=200, height=1, highlightthickness=1,
                            highlightbackground=PALETTE["main"]["2color"],
                            background=PALETTE["secondary"]["1color"],
                             )
        line_canvas.place(x=-4, y=445)
        line_canvas.create_line(50, 100, 350, 100)

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
        add_button.place(x=6, y=465)

        category_add = lambda: self.cat_setup.create_interface_edit_category_win()
        edit_button = Button(self.side_frame, text="Edit category",
                             bg=PALETTE["main"]["1color"],
                             font=("Arial", 14),
                             fg=PALETTE["text"]["2color"],
                             activebackground=PALETTE["main"]["3color"],
                             activeforeground=PALETTE["text"]["1color"],
                             width=175, height=18,
                             border=4, relief="flat",
                             command=category_add
                             )
        edit_button.place(x=6, y=500)

        category_delete = lambda: self.cat_delete.create_message_delete_category()
        delete_button = Button(self.side_frame, text="Delete category",
                               bg=PALETTE["main"]["1color"],
                               font=("Arial", 14),
                               fg=PALETTE["text"]["2color"],
                               activebackground=PALETTE["main"]["3color"],
                               activeforeground=PALETTE["text"]["1color"],
                               width=175, height=18,
                               border=4, relief="flat",
                               command=category_delete
                               )
        delete_button.place(x=6, y=535)

        before_link_text = Label(text="Our git: ",
                                 bg=PALETTE["main"]["2color"],
                                 font=("Arial", 14),
                                 fg=PALETTE["text"]["1color"],
                                 )
        before_link_text.place(x=19, y=572)
        my_link_in_browser = Label(text="app-Quick-Notes",
                                   bg=PALETTE["main"]["2color"],
                                   font=("Arial", 14),
                                   fg=PALETTE["secondary"]["1color"],
                                   activeforeground=PALETTE["text"]["2color"]
                                   )
        my_link_in_browser.place(x=71, y=572)
        my_link_in_browser.bind("<Button-1>", lambda e: self.open_link())

    @staticmethod
    def open_link():
        url = "https://github.com/nikitach507/app-Quick-Notes"
        webbrowser.open_new(url)
