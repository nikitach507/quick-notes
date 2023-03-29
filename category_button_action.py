import tkinter

from database.category_database_action import CategoryDatabaseAction
from main import *


class CategoryButtonAction:
    def __init__(self, root):
        self.root = root
        self.active_item = 0
        self.side_listbox_categories = None
        self.side_listbox_active_category = None

    def settings_category(self, test_x, test_y):
        Label(self.root, bg="#F1EBD8", border=4, relief="sunken").place(x=190, y=55, relwidth=1, relheight=1)

        side_frame_categories = Frame(self.root)
        side_frame_categories.place(x=test_x, y=test_y)

        self.side_listbox_categories = Listbox(side_frame_categories, width=12, height=15,
                                               font=("Georgia", 20), fg="black",
                                               bg="#E4BA6A", border=3, relief="flat", )

        side_scrollbar_categories = Scrollbar(side_frame_categories)
        side_scrollbar_categories.configure(command=self.side_listbox_categories.yview)

        self.side_listbox_categories.configure(yscrollcommand=side_scrollbar_categories.set)

        # Getting all categories into a list from the database
        all_database_categories = CategoryDatabaseAction.all_categories_list("note_category")
        all_database_categories.insert(0, "All notes")

        # Add the resulting categories to the area
        for category in all_database_categories:
            self.side_listbox_categories.insert(END, category)

        # Bind event handlers to the list
        self.side_listbox_categories.bind("<<ListboxSelect>>", self.on_select_side_listbox)
        self.side_listbox_categories.bind("<ButtonRelease-1>", self.on_release_side_listbox)

        # Set the default active item
        self.side_listbox_categories.selection_set(0)
        self.update_color_side_listbox()
        self.side_listbox_categories.pack(side=LEFT, fill=BOTH, expand=True)

        if len(all_database_categories) > 15:
            side_scrollbar_categories.pack(side=LEFT, fill=Y)

    def on_select_side_listbox(self, event):
        # List item selection event handler
        widget = event.widget
        selection = widget.curselection()
        if selection:
            item_index = selection[0]
            if item_index != self.active_item:
                self.side_listbox_categories.selection_clear(self.active_item)
                self.active_item = item_index
                self.update_color_side_listbox()
                self.side_listbox_active_category = widget.get(self.active_item)
                # self.note_display_interface(self.side_listbox_active_category)

    def on_release_side_listbox(self, event):
        # Mouse button release event handler
        widget = event.widget
        item_index = widget.nearest(event.y)
        if item_index != self.active_item:
            self.side_listbox_categories.selection_clear(self.active_item)
            self.active_item = item_index
            self.side_listbox_categories.selection_set(self.active_item)
            self.update_color_side_listbox()

    def update_color_side_listbox(self):
        # Updating the color of the active item
        for item in range(self.side_listbox_categories.size()):
            if item == self.active_item:
                self.side_listbox_categories.itemconfig(item, bg="#F2D9AA", fg="#4C5117",
                                                        selectbackground="#F2D9AA", selectforeground="#4C5117")
            else:
                self.side_listbox_categories.itemconfig(item, bg="#E4BA6A", fg="#3C4013",
                                                        selectbackground="#FBF5E3", selectforeground="#787D46")